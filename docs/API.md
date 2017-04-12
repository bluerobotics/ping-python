# Ping API Reference


## Table of Conents

* [Accessor Methods]()
  * [getDistance()]()

-----


## Accessor Methods

These methods are used to acquire data from the device. They return a named tuple which can be used to access specific fields. 

`code example here`

-----

### `getDistance()`

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

### `getDistanceSimple()`

Returns the most recent distance reading and confidence. Provides no advantage over the full `getDistance()` message

| Item          | Description                                        |
|---------------|----------------------------------------------------|
| distance      | Nearest object to Ping                             |
| confidence    | Confidence in the measurement, as a percent        |

<br/>
<br/>

### `getProfile()`

Returns the latest distance reading data. Includes all metadata. 

| Item               | Description                                        |
|--------------------|----------------------------------------------------|
| distance           | Nearest object to Ping                             |
| confidence         | Confidence in the measurement, as a percent        |
| pulse_usec         | Length of the sent pulse, in microseconds          |
| ping_number        | Counts the pings since startup                     |
| start_mm           | Closest distance that Ping was scanning            |
| length_mm          | Length of scanning range                           |
| gain_index         | Receiving gain index                               |
| num_points         | Number of data points                              |
| points[num_points] | Array of profile data points                       |

<br/>
<br/>

### `getRange()`

Returns information about the range that Ping is scanning in.

| Item          | Description                                        |
|---------------|----------------------------------------------------|
| start_mm      | Closest distance that Ping was scanning            |
| length_mm     | Confidence in the measurement, as a percent        |

<br/>
<br/>

### `getMode()`

Returns whether Ping is in auto or manual mode.

| Item             | Description                                        |
|------------------|----------------------------------------------------|
| auto_manual      | 1 = auto, 0 = manual                               |

<br/>
<br/>

### `getRate()`

Returns the ping rate, in Hz.

<br/>
<br/>

### `getGain()`

Retuns the index of the receiving analog gain. See table below for reference.

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

### `getPulseLength()`

Returns the sent pulse length.

<br/>
<br/>

## Control Methods


### `setRange()`

Sets information about the range that Ping is scanning in.

| Item          | Description                                        |
|---------------|----------------------------------------------------|
| start_mm      | Closest distance that Ping was scanning            |
| length_mm     | Confidence in the measurement, as a percent        |

<br/>
<br/>

### `setMode()`

Sets whether Ping is in auto or manual mode.

| Item             | Description                                        |
|------------------|----------------------------------------------------|
| auto_manual      | 1 = auto, 0 = manual                               |

<br/>
<br/>

### `setRate()`

Sets the ping rate, in Hz.

<br/>
<br/>

### `setGain()`

Sets the index of the receiving analog gain. See table below for reference.

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

### `setPulseLength()`

Sets the sent pulse length.

<br/>
<br/>


