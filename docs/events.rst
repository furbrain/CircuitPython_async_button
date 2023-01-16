Events
======

The `Button` object can detect single, double, triple and long clicks. The ``double_click_max_duration`` parameter
determines how close together clicks have to be before they are considered a double click (or triple click). A long
click is fired after the button has been pressed for ``long_click_min_duration`` seconds. Note that the button does
not have to be released for this to happen, and you do not receive a single/double/triple click after that.

The following timing diagrams demonstrate what events are triggered depending on which params have been set.
(``t_double`` is `double_click_max_duration` and ``t_long`` is `long_click_min_duration`)

Single click mode
-----------------

.. wavedrom:: ./timing_single.json
    :width: 500px
    :caption: double_click_enable=False, triple_click_enable=False
    :name: single_click

Double click mode
-----------------

.. wavedrom:: ./timing_double.json
    :caption: double_click_enable=True, triple_click_enable=False

Triple click mode
-----------------

.. wavedrom:: ./timing_triple.json
    :caption: double_click_enable=True, triple_click_enable=True

Long click mode
---------------

.. wavedrom:: ./timing_long.json
    :caption: long_click_enable=True
