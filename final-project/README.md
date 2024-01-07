## Example request

```json
{
    "model_name": "osm",
    "source": {
        "shape": {
            "x": 5,
            "y": 5
        },
        "event_element_count": 1
    },
    "target": {
        "shape": {
            "x": 30,
            "y": 30
        }
    },
    "obstacles": [
        {
            "id": 29,
            "shape": {
                "x": 25,
                "y": 15,
                "width": 1,
                "height": 5
            }
        },
        {
            "id": 28,
            "shape": {
                "x": 20,
                "y": 15,
                "width": 2,
                "height": 5
            }
        }
    ]
}
```