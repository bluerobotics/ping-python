#Ping API Reference

##Methods

* `getResults()`

Returns list of all results from last ping. Each point is on a scale of 0 to 255
<br/>
<br/>

* `getDepth()`

Returns the most recent smoothed depth reading in mm
<br/>
<br/>

* `getConfidence()`

Returns the confidence in the depth measurement, as a percentage
<br/>
<br/>

* `getInstantDepth()`

Returns the best guess for this individual ping in mm. It is recommended to use getDepth() instead
<br/>
<br/>

* `getStartDepth()`

Returns the shallowest depth that Ping will look at, in mm
<br/>
<br/>

* `getDepthRange()`

Returns the range of depth that is being scanned in mm. Beginning at the start depth
<br/>
<br/>

* `getVersion()`

Returns a string of Ping's firmware version number
<br/>
<br/>

* `getNumResults()`

Returns the number of data points in the last ping
<br/>
<br/>

* `getVoltage()`

Returns the operating voltage in mV. Expected to be around 5000mV
<br/>
<br/>

* `getPingDuration()`

Returns the duration of the sent ping, in microseconds
<br/>
<br/>

* `getGain()`

Retuns the index of the analog gain
<br/>
<br/>

* `getPingNumber()`

Returns the number of pings that Ping has sent
<br/>
<br/>

* `getTimestamp()`

Returns the uptime, in milliseconds
<br/>
<br/>

* `getBottomIndex()`

Returns the index of the depth reading that was chosen as the bottom
