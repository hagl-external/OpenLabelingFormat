from google.cloud import firestore

def history():
    history = {
        "created": {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "dateTime": "1996-12-19T16:39:57.23-08:00"
        },
        "modified": {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "dateTime": "1996-12-19T16:39:57.23-08:00"
        }
    }
    return history

def versionInfo():
    version_info = {
        "schema": "0.2",
        "labelFile": "0.1",
        "history": history()
    }
    return version_info

def projectInfo():
    project_info = {
        "unit": "frames",
        "history": history,
        "start": 0.0,
        "end": 100.0,
        "skip": 22.0
    }
    return project_info

def mediaInfo():
    media_info = [
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "history": history(),
            "name": "ABCDEF",
            "url": "ABCDEFGHI",
            "hash": {
                "value": "ABCDEFGHIJKLMN",
                "method": "md5"
            },
            "type": "video/mp4",
            "codec": "ABCDEFGHIJ",
            "duration": 495.5,
            "framerate": 829,
            "width": 135,
            "height": 216
        }
    ]
    return media_info

def calibrationInfo():
    calibration_info = {
       "uuid": "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJ",
       "name": "ABCDEFGHIJKLMNOPQRSTUVWXYZA",
       "url": "ABCDEFGHIJKLMN",
       "hash": {
           "value": "ABCDEFGHIJKLMNOPQRSTUVWXY",
           "method": "sha-256"
       },
       "history": history(),
        "coordinateSystem": {
            "coordinateSystem2D": {
                "translation": {
                    "x": 0.0,
                    "y": 0.0,
                    "unit": "px"
                },
                "rotation": {
                    "angle": 0.0,
                    "unit": "rad"
                }
            }
        }
    }
    return calibration_info

def odometryInfo():
    odometry_info = {
        "uuid": "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJ",
        "name": "ABCDEFGHIJKLMNOPQ",
        "url": "ABCDEFGHIJKLMN",
        "hash": {
            "value": "ABCDEFGHIJKLMN",
            "method": "sha-224"
        },
        "history": history()
    }
    return odometry_info

def positionInfo():
    position_info = {
        "uuid": "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJ",
        "name": "ABCDEFGHIJKLMNOPQRSTUV",
        "url": "ABCDEFGHIJKLMNOPQRSTUV",
        "hash": {
            "value": "ABCDE",
            "method": "sha-224"
        },
        "history": history()
    }
    return position_info

def metaInfo():
    meta_info = [
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "weather",
            "name": "rainy",
            "value": "none",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "weather",
            "name": "snowy",
            "value": "none",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "weather",
            "name": "cloudy",
            "value": "none",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "weather",
            "name": "foggy",
            "value": "none",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "weather",
            "name": "sunny",
            "value": "none",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "visibility",
            "name": "clear",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "rangeOfSight",
            "name": "100m-500m",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "roadType",
            "name": "city",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        },
        {
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "type": "roadCondition",
            "name": "good",
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "history": history()
        }
    ]
    return meta_info

def objectInfo():
    object_info = [
        {
            "objectid": -1,
            "uuid": "00000000-0000-0000-C000-000000000046",
            "uuidOfMedia": "00000000-0000-0000-C000-000000000046",
            "history": history(),
            "validity": {
                "start": 0.0,
                "end": 1000.0,
                "unit": "frames"
            },
            "attributes": [
                {
                    "uuid": "00000000-0000-0000-C000-000000000046",
                    "type": "truncation",
                    "name": "<=25%"
                },
                {
                    "uuid": "00000000-0000-0000-C000-000000000046",
                    "type": "occlusion",
                    "name": "<=25%"
                },
                {
                    "uuid": "00000000-0000-0000-C000-000000000046",
                    "type": "type",
                    "name": "pedestrian"
                }
            ],
            "shapes": [
                {
                    "box2D": {
                        "topLeft": {
                            "x": 0.0,
                            "y": 42.0,
                            "unit": "px"
                        },
                        "bottomRight": {
                            "x": 50.0,
                            "y": 100.0,
                            "unit": "px"
                        },
                        "rotation": {
                            "angle": 0.0,
                            "unit": "rad"
                        }
                    }
                }
            ],
            "relations": [
                {
                    "uuidOfSibling": "00000000-0000-0000-C000-000000000046"
                },
                {
                    "uuidOfParent": "00000000-0000-0000-C000-000000000046"
                }
            ]
        }
    ]
    return object_info

def exportLabelsAsOLF(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    db = firestore.Client()

    request_json = request.get_json()

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'