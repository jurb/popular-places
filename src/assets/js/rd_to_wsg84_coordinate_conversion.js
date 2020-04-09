// coordinateconversion.js

// Functions to convert coordinates:
// - Dutch Rijksdriehoek coordinates (R/D, EPSG:28992)
// - WGS84 coordinates (latitude/longitude, EPSG:4326).
// - Mercator meters (EPSG:54004)

// Convert Rijksdriehoek (R/D) coordinates to WGS (lat/lon) coordinates.

module.exports = rd2Wgs;
module.exports.default = rd2Wgs;

function rd2Wgs(rdX, rdY) {
  // This calculation was based from the sourcecode of Ejo Schrama's software <schrama@geo.tudelft.nl>.
  // You can find his software on: http://www.xs4all.nl/~digirini/contents/gps.html

  // Fixed constants / coefficients
  var x0 = 155000;
  var y0 = 463000;
  var k = 0.9999079;
  var bigr = 6382644.571;
  var m = 0.003773954;
  var n = 1.000475857;
  var lambda0 = 0.094032038;
  var phi0 = 0.910296727;
  var l0 = 0.094032038;
  var b0 = 0.909684757;
  var e = 0.081696831;
  var a = 6377397.155;

  // Convert RD to Bessel

  // Get radius from origin.
  var d_1 = rdX - x0;
  var d_2 = rdY - y0;
  var r = Math.sqrt(Math.pow(d_1, 2) + Math.pow(d_2, 2)); // Pythagoras

  // Get Math.sin/Math.cos of the angle
  var sa = r != 0 ? d_1 / r : 0; // the if prevents devision by zero.
  var ca = r != 0 ? d_2 / r : 0;

  var psi = Math.atan2(r, k * 2 * bigr) * 2; // php does (y,x), excel does (x,y)
  var cpsi = Math.cos(psi);
  var spsi = Math.sin(psi);

  var sb = ca * Math.cos(b0) * spsi + Math.sin(b0) * cpsi;
  var d_1 = sb;

  var cb = Math.sqrt(1 - Math.pow(d_1, 2)); // = Math.cos(b)
  var b = Math.acos(cb);

  var sdl = (sa * spsi) / cb; // = Math.sin(dl)
  var dl = Math.asin(sdl); // delta-lambda

  var lambda_1 = dl / n + lambda0;
  var w = Math.log(Math.tan(b / 2 + Math.PI / 4));
  var q = (w - m) / n;

  // Create first phi and delta-q
  var phiprime = Math.atan(Math.exp(q)) * 2 - Math.PI / 2;
  var dq_1 =
    (e / 2) *
    Math.log((e * Math.sin(phiprime) + 1) / (1 - e * Math.sin(phiprime)));
  var phi_1 = Math.atan(Math.exp(q + dq_1)) * 2 - Math.PI / 2;

  // Create new phi with delta-q
  var dq_2 =
    (e / 2) * Math.log((e * Math.sin(phi_1) + 1) / (1 - e * Math.sin(phi_1)));
  var phi_2 = Math.atan(Math.exp(q + dq_2)) * 2 - Math.PI / 2;

  // and again..
  var dq_3 =
    (e / 2) * Math.log((e * Math.sin(phi_2) + 1) / (1 - e * Math.sin(phi_2)));
  var phi_3 = Math.atan(Math.exp(q + dq_3)) * 2 - Math.PI / 2;

  // and again...
  var dq_4 =
    (e / 2) * Math.log((e * Math.sin(phi_3) + 1) / (1 - e * Math.sin(phi_3)));
  var phi_4 = Math.atan(Math.exp(q + dq_4)) * 2 - Math.PI / 2;

  // radians to degrees
  var lambda_2 = (lambda_1 / Math.PI) * 180; //
  var phi_5 = (phi_4 / Math.PI) * 180;

  // Bessel to wgs84 (lat/lon)
  var dphi = phi_5 - 52; // delta-phi
  var dlam = lambda_2 - 5; // delta-lambda

  var phicor = (-96.862 - dphi * 11.714 - dlam * 0.125) * 0.00001; // correction factor?
  var lamcor = (dphi * 0.329 - 37.902 - dlam * 14.667) * 0.00001;

  var phiwgs = phi_5 + phicor;
  var lamwgs = lambda_2 + lamcor;

  // Return as anonymous object
  return [phiwgs, lamwgs];
}
