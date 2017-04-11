# Ping API Reference

## Accessor Methods

These methods are used to acquire data from the device

-----

* `getDistance()`

Returns the latest distance reading data. Includes all metadata. 

| Item          | Description                                        |
|---------------|----------------------------------------------------|
| distance      | Nearest object to Ping                             |
| confidence    | Confidence in the measurement, as a percent        |
| pulse_usec    | Length of the sent pulse, in microseconds          |
| ping_number   | Counts the pings since startup                     |
| start_mm      | Closest distance that Ping was scanning            |
| length_mm     | Length of scanning range                           |
| gain_index    | Receiving gain index                               |

<br/>
<br/>

* `getDistanceSimple()`

Returns the most recent distance reading and confidence. 
<br/>
<br/>

* `getRange())`

Description
<br/>
<br/>

* `getMode()`

Description
<br/>
<br/>

* `getRate()`

Description
<br/>
<br/>

* `getGain()`

Description
<br/>
<br/>

* `getPulseLength()`

Description
<br/>
<br/>

* `getGain()`

Retuns the index of the analog gain

| Index | Gain (dB) |
|-------|-----------|
|     0 |      -6.6 |
|     1 |         3 |
|     2 |      12.6 |
|     3 |        20 |
|     4 |      27.4 |
|     5 |        37 |
|     6 |      44.4 |
|     7 |      50.6 |
|     8 |        58 |
|     9 |        64 |

<br/>
<br/>
