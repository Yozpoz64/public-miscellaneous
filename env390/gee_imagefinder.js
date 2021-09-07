var CLOUDPERCENT = 10
var EARLIEST = true
var SPATIALRES = 30
var NUMPIXELS = 5000
var COVERAGEPERCENT = 100
var STARTYEAR = 1999
var ENDYEAR = 2021
var DEBUG = false

print(AOI.coordinates())
/*
NOTES
-landsat 7 only has a few images that have complete coverage (1999, 2000)
*/

// function for returning an image from L7 imagecollection (with params)
//    should I be getting the median?
function getImage(year, cloudPercent, earliest) {
  var startDate = year + '-01-01'
  var endDate = year + '-12-31'
  var images = //ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
               ee.ImageCollection("LANDSAT/LT05/C01/T1_SR") 
                .filterBounds(AOI)
                .filterMetadata('CLOUD_COVER', 'less_than', cloudPercent)
                .filterDate(startDate, endDate)
                //.sort('SENSING_TIME', earliest)
                
  // this is a very ugly solution, work in progress
  if (images.size().getInfo() == 0) {
    var images = ee.ImageCollection("LANDSAT/LE07/C01/T1_SR")
                .filterBounds(AOI)
                .filterMetadata('CLOUD_COVER', 'less_than', cloudPercent)
                .filterDate(startDate, endDate)
  }
  
  if (images.size().getInfo() == 0) {
    var images = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
                .filterBounds(AOI)
                .filterMetadata('CLOUD_COVER', 'less_than', cloudPercent)
                .filterDate(startDate, endDate)
  }
  return images
  
}

// gets percentage cover of satellite image to area of interest
// modified from: https://gis.stackexchange.com/questions/354398/filter-imagecollection-to-images-with-non-masked-coverage-within-aoi-in-earth-en
function getCover(image, aoi, scale) {

    // calculate the number of inputs 
    var totPixels = ee.Number(image.unmask(1).reduceRegion({
      reducer: ee.Reducer.count(),
      scale: scale,
      geometry: aoi,
    }).values().get(0));

    // Calculate the actual amount of pixels inside the aoi
    var actPixels = ee.Number(image.reduceRegion({
      reducer: ee.Reducer.count(),
      scale: scale,
      geometry: aoi,    
    }).values().get(0));

    // calculate the perc of cover
    var percCover = actPixels.divide(totPixels).multiply(100).round();

  // number as output
  return image.set('percCover', percCover);
}

// returns normalised difference of two input bands on input image
function getNormDif(image, bands) {
  return image.normalizedDifference(bands)
}

// perform unsupervised classification
function usClassify(image, spatialRes, numPixels, classes, label, palette) {
  var training = image.sample({
    region: AOI,
    scale: spatialRes,
    numPixels: numPixels
  })
  var clusterer = ee.Clusterer.wekaKMeans(classes).train(training)
  var result = image.cluster(clusterer)
  Map.addLayer(result.clip(AOI), {min: 0, max: (classes - 1), palette: palette}, label)
}

// run all analyses in order
function analyze(year, type, classes, colours) {
  var useableImage = true
  
  // get image collection
  var images = getImage(year, CLOUDPERCENT, EARLIEST)
  if (DEBUG) {print('images in ' + year + ': ' + images.size().getInfo())}
  
  if (!images.size().getInfo() == 0) {
    // get and set image coverage
    var imagesWithCoverage = images.map(function(image){
      return getCover(image, AOI, 30)})
    
    var image = imagesWithCoverage.sort('percCover', false).first()
    var thisCoverage = image.get('percCover').getInfo()
    
    if (thisCoverage != COVERAGEPERCENT) {
      if (DEBUG) {print('Coverage not high enough')}
      useableImage = false
    }
  } else {
    useableImage = false
  }
  
  if (useableImage){
    // set label based on arguments
    var satellite = image.get('SATELLITE').getInfo()
    var label = type + ' (' + year + ', ' + classes + ' classes, ' + satellite + ')'
    
    // set bands based on input string
    var bands = []
    
    // conditional indicies for band allocations based on satelllite CONTINUE HERE
    // nir, swir, green
    var nir = ''
    var swir = ''
    var green = ''
    if (satellite == 'LANDSAT_5') {
        nir = 'B4'
        swir = 'B5'
        green = 'B2'
    } else if (satellite == 'LANDSAT_7') {
        nir = 'B4'
        swir = 'B5'
        nir = 'B2'
    } else if (satellite == 'LANDSAT_8') {
        nir = 'B5'
        swir = 'B6'
        nir = 'B3'
    }
    
    if (type == 'NDWI') {
      bands = [green, nir]
    } else if (type == 'NDMI') {
      bands = [nir, swir]
    } else if (type == 'MNDWI') {
      bands = [green, swir]
    }
      
    // get normalised index
    var imageIndex = getNormDif(image, bands)
    
    // show true colour images if bool true
    if (DEBUG) {
      Map.addLayer(image.clip(AOI), {bands: ['B3', 'B2', 'B1'], min: 0, max: 3000}, 
                              ('True colour (' + year + ')'))
    }
    
    // perform classification
    usClassify(image, SPATIALRES, NUMPIXELS, classes, label, colours)
  }
}

var AOI = ee.Geometry.Polygon(ee.List([[170.4326055443,-45.9393522244],[170.4291723167,-45.9025720245],[170.6385991966,-45.8887134207],[170.6488988792,-45.8901472297],[170.6482122337,-45.9202486702],[170.5253026878,-45.9255028035],[170.4326055443,-45.9393522244]]))

var currentYear = STARTYEAR

while (currentYear != (ENDYEAR + 1)) {
  analyze(currentYear, 'NDMI', 2, ['brown', 'blue'])
  currentYear += 1
}
 



Map.centerObject(AOI)