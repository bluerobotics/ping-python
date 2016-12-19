#Ping API Reference

##Accessor Methods

These methods are used to acquire data from the device

-----

* `getResults()`

Returns list of all results from last ping. Each point is on a scale of 0 to 255
<br/>
<br/>

* `getDistance()`

Returns the most recent smoothed distance reading in mm
<br/>
<br/>

* `getConfidence()`

Returns the confidence in the distance measurement, as a percentage
<br/>
<br/>

* `getInstantDistance()`

Returns the best guess for this individual ping in mm. It is recommended to use getDistance() instead
<br/>
<br/>

* `getScanStart())`

Returns the closest that Ping will look at, in mm
<br/>
<br/>

* `getScanRange()`

Returns the range that is being scanned in mm. Beginning at the start distance
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

Returns the index of the reading that was chosen as the result
##Control Methods

These methods are to control the device. Leave any argument as 0 to ignore, or leave as the default.

-----

* `sendConfig(rate, cWater)`

Sends configuration options to Ping. See [here](http://keisan.casio.com/exec/system/1258122391) for determining the speed of sound in water. This depends on salinity and temperature!

|    Argument     |    Value    |             Result             |
|-----------------|-------------|--------------------------------|
| rate            | 0           | Default / unchanged            |
|                 | 1           | Single                         |
|                 | 2           | Continuous with Automatic rate |
| cWater          | 0           | Default / unchanged            |
|                 | 1000 - 2000 | Sets the speed of sound in m/s |

<br/>
<br/>

* `sendRequest(messageID)`

Requests a message from Ping. See the [Serial Protocol](http://github.com/bluerobotics/ping-python/blob/master/docs/Format.md) for message formats.

|      Argument      | Value |  Result  |
|--------------------|-------|----------|
| messageID          | 0x01  | distance |
|                    | 0x02  | profile  |
|                    | 0x03  | status   |


<br/>
<br/>


* `sendRange(auto, start, range)`

Set the range that Ping will scan for the bottom. If manual mode is set, you may specify the start distance and range that Ping will scan, or set 0 to leave those values unchanged.

|    Argument    |   Value     |               Result               |
|----------------|-------------|------------------------------------|
| auto           | 0           | Automatic scanning range           |
|                | 1           | Manual scanning range              |
| start          | 0           | Default / unchanged                |
|                | 1 - 60000   | Set start distance in mm              |
| range          | 0           | Default / unchanged                |
|                | 500 - 60000 | Set length of scanning range in mm |

<br/>
<br/>
