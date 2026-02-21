# Changelog

## 0.3.1
### Bug Fixes
 - Handle scenario where head unit is connected but does not have a valid GPS fix and returns (0, 0)

## 0.3.0

### Breaking Changes
 - `rcttools` now requires `ffmpeg >= 7` (released April, 2024) [#12](https://github.com/qwhelan/rcttools/pull/12), [#25](https://github.com/qwhelan/rcttools/pull/25)

### Bug Fixes
 - The initial, unstacked parsing process was rejecting validly processed frames due to the pass threshold being set too high. As we expect the stacking process to clean things up considerably, lowered initial threshold to 0.4 from 0.8 [#13](https://github.com/qwhelan/rcttools/pull/13)
 - Specify the frame rate of the color streams being fed to the threshold filter, resolving an issue where an extra frame was being injected into the output due to a frame rate mismatch [#17](https://github.com/qwhelan/rcttools/pull/17)
 - Specify the frame rate of the input stream, resolving the other source of an extra frame being injected [#18](https://github.com/qwhelan/rcttools/pull/18)
 - Handle two-digit longitudes correctly by adding `.` to the alphabet and adjusting state machine logic [#21](https://github.com/qwhelan/rcttools/pull/21)

### New Features
 - Headings are now estimated based on GPS track, combined with the assumption that a RCT715 is mounted directly rear-facing [#16](https://github.com/qwhelan/rcttools/pull/16)
 - Handle scenario where RCT715 loses connection with head unit and thus has time data but no GPS data [#22](https://github.com/qwhelan/rcttools/pull/22)
 - Make non-existent input easier to debug for end user and suppress traceback [#26](https://github.com/qwhelan/rcttools/pull/26)
 - Document that only 1080p video is currently supported [#27](https://github.com/qwhelan/rcttools/pull/27)

### Testing
 - Add test harness for testing specific, problematic data frames and adjust score threshold for borderline cases [#20](https://github.com/qwhelan/rcttools/pull/20)

### Other Changes
 - Miscellaneous updates to dependencies
 - Add `CHANGELOG.md` [#28](https://github.com/qwhelan/rcttools/pull/28)

### Contributors
 - [@qwhelan](https://github.com/qwhelan)