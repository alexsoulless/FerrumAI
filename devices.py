# DEVICES = {
#     "лампочка гостинная": {
#         "включить": "/room1/lamp/on",
#         "выключить": "/room1/lamp/off",
#     },
#     "чайник кухня": {"вскипятить воду", "/kitchen/teapod/boil"},
#     "датчик температуры гостинная": {"измерить температуру", "/room1/temp_sensor/get"},
#     "лампочка ванная": {"включить": "/room2/lamp/on", "выключить": "/room2/lamp/on"},
# }

DEVICES = {
    "лампочка гостинная": ["/room1/lamp/on", "/room1/lamp/off"],
    "чайник кухня": ["/kitchen/teapod/boil_water"],
    "датчик температуры гостинная": ["измерить температуру", "/room1/temp_sensor/get"],
    "лампочка ванная": ["/room2/lamp/on", "/room2/lamp/on"],
}
