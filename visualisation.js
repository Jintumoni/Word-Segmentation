/*
This is a p5.js code to visualise how we arrive at the CSF formula

paste this in https://editor.p5js.org/ to play around
*/

let EPS = 10e-9;
let INF = 10e18;

function setup() {
  createCanvas(800, 800);
}

function sigmoid(x) {
  return 1 / (1 + exp(-x));
}

function getDistance(x1, y1, x2, y2) {
  return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

function getDistanceBetweenBox(box1, box2) {
  let x1Min = box1[0];
  let y1Min = box1[1];
  let x1Max = box1[2];
  let y1Max = box1[3];
  let x2Min = box2[0];
  let y2Min = box2[1];
  let x2Max = box2[2];
  let y2Max = box2[3];
  
  let DISTANCE = {
    x1:0,
    y1:0,
    x2:0,
    y2:0,
    distance:0
  };
  
  if (y2Max < y1Min) {
    // box1 below box2
    if(x2Min > x1Max) {
      // box1 on left side
      DISTANCE.x1 = x1Max;
      DISTANCE.y1 = y1Min;
      DISTANCE.x2 = x2Min;
      DISTANCE.y2 = y2Max;
      DISTANCE.distance = getDistance(x1Max, y1Min, x2Min, y2Max);
      return DISTANCE;
    }
    else if(x2Max < x1Min) {
      // box1 on right side
      DISTANCE.x1 = x1Min;
      DISTANCE.y1 = y1Min;
      DISTANCE.x2 = x2Max;
      DISTANCE.y2 = y2Max;
      DISTANCE.distance = getDistance(x1Min, y1Min, x2Max, y2Max);
      return DISTANCE;
    }
    else {
      // box1 in-between
      DISTANCE.x1 = x1Min;
      DISTANCE.y1 = y1Min;
      DISTANCE.x2 = x1Min;
      DISTANCE.y2 = y2Max;
      DISTANCE.distance = y1Min - y2Max;
      return DISTANCE;
    }
  }
  else if(y1Max < y2Min) {
    // box1 above box2
    if(x2Min > x1Max) {
      // box1 on left
      DISTANCE.x1 = x1Max;
      DISTANCE.y1 = y1Max;
      DISTANCE.x2 = x2Min;
      DISTANCE.y2 = y2Min;
      DISTANCE.distance = getDistance(x1Max, y1Max, x2Min, y2Min);
      return DISTANCE;
    }
    else if(x2Max < x1Min) {
      // box1 on right
      DISTANCE.x1 = x1Min;
      DISTANCE.y1 = y1Max;
      DISTANCE.x2 = x2Max;
      DISTANCE.y2 = y2Min;
      DISTANCE.distance = getDistance(x1Min, y1Max, x2Max, y2Min);
      return DISTANCE;
    }
    else {
      // box1 in-between
      DISTANCE.x1 = x1Min;
      DISTANCE.y1 = y1Max;
      DISTANCE.x2 = x1Min;
      DISTANCE.y2 = y2Min;
      DISTANCE.distance = y2Min - y1Max;
      return DISTANCE;
    }
  }
  else {
    if(x2Min > x1Max) {
      // box1 on left side (parallel)
      DISTANCE.x1 = x1Max;
      DISTANCE.y1 = y1Min;
      DISTANCE.x2 = x2Min;
      DISTANCE.y2 = y1Min;
      DISTANCE.distance = x2Min - x1Max;
      return DISTANCE;
    }
    else if(x2Max < x1Min) {
      // box1 on right side (parallel)
      DISTANCE.x1 = x1Min;
      DISTANCE.y1 = y1Min;
      DISTANCE.x2 = x2Max;
      DISTANCE.y2 = y1Min;
      DISTANCE.distance = x1Min - x2Max;
      return DISTANCE;
    }
    else {
      // overlap
      DISTANCE.x1 = (x1Min + x1Max) / 2;
      DISTANCE.y1 = (y1Min + y1Max) / 2;
      DISTANCE.x2 = (x2Min + x2Max) / 2;
      DISTANCE.y2 = (y2Min + y2Max) / 2;
      DISTANCE.distance = 0;
      return DISTANCE;
    }
  }
}

function getSlope(x1, y1, x2, y2) {
  let slope = (y2 - y1) / (x2 - x1 + EPS);
  return abs(atan(slope)) * 180 / PI;
}

function getSlopeFactor(slope) {
  return 50 * exp(-slope * slope / 150);
  // return -pow(slope, 2) / 10 + 50;
}

function getDistanceFactor(distance) {
  //return 100 * exp(-sqrt(distance) / 10) - 50;
  return -pow(distance, 2) / 1000 + 50;
}

function calculateStrength(x1, y1, x2, y2, D) {
  let slope = getSlope(x1, y1, x2, y2);
  let slopeFactor = getSlopeFactor(slope);
  
  let distance = D;
  let distanceFactor = getDistanceFactor(distance);

  let CSF = (slopeFactor + distanceFactor);
  return CSF - 50;
}



function draw() {
  fill(240);
  background(220);
  let rectWidth = 120;
  let rectHeight = 70;
  let topX = 200;
  let topY = 230;
  rect(topX, topY, rectWidth, rectHeight);  
  
  let rectX = mouseX - rectWidth / 2; 
  let rectY = mouseY - rectHeight / 2; 

  rect(rectX, rectY, rectWidth, rectHeight); 
  
  let box2 = [topX, topY, topX + rectWidth, topY + rectHeight];
  let box1 = [rectX, rectY, rectX + rectWidth, rectY + rectHeight];
  let coordinates = getDistanceBetweenBox(box1, box2);
  
  stroke(255, 0, 0);
  line(coordinates.x1, coordinates.y1, coordinates.x2, coordinates.y2);
  
  noStroke();
  fill(0);
  textSize(15);
  textAlign(CENTER);
  
  // let distance = getDistance(topX + rectWidth / 2, topY + rectHeight / 2, mouseX, mouseY);
  let distance = coordinates.distance;
  let distanceFactor = getDistanceFactor(distance);
  
   let CSF = calculateStrength(topX + rectWidth / 2, topY + rectHeight / 2, mouseX, mouseY, distance);
  let slope = getSlope(topX + rectWidth / 2, topY + rectHeight / 2, mouseX, mouseY);
  let slopeFactor = getSlopeFactor(slope);
  
  
  text("CSF = " + CSF, width/2, 30); 
  text("Slope = " + round(slope,1) + " degrees", width/2 - 100, 50);
  text("Distance = " + round(distance,1), width/2 - 100, 70);
  text("SlopeFactor = " + round(slopeFactor,1), width/2 + 100, 50);
  text("DistanceFactor = " + round(distanceFactor,1), width/2 + 100, 70);
}
