import json
import pytest
from unittest.mock import MagicMock, patch
import datetime as dt

from hyundai_kia_connect_api.KiaUvoApiCA import KiaUvoApiCA
from hyundai_kia_connect_api.Token import Token
from hyundai_kia_connect_api.Vehicle import Vehicle
from hyundai_kia_connect_api.ApiImpl import ScheduleChargingClimateRequestOptions
from hyundai_kia_connect_api.const import ENGINE_TYPES, OFF_PEAK_MODE, CLIMATE_HEATING_LEVEL

@pytest.fixture
def api():
    return KiaUvoApiCA(region=2, brand=1, language="en")

@pytest.fixture
def token():
    return Token(
        username="test_user",
        password="test_password",
        access_token="test_access_token",
        refresh_token="test_refresh_token",
        valid_until=dt.datetime.now() + dt.timedelta(hours=1),
        pin="1234"
    )

@pytest.fixture
def vehicle():
    return Vehicle(
        id="test_vehicle_id",
        name="test_vehicle",
        model="EV6",
        year=2022,
        VIN="test_vin",
        engine_type=ENGINE_TYPES.EV
    )

TEST_CASES = [
    (
        "Disabled",
        ScheduleChargingClimateRequestOptions(),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "0",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [9],
                            "time": {"time": "1200", "timeSection": 0}
                        },
                        "reservChargeSet": False,
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [9],
                            "time": {"time": "1200", "timeSection": 0}
                        },
                        "reservChargeSet": False
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 0,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
    (
        "Enabled - Departure 1 - Without climate - Without off peak charging",
        ScheduleChargingClimateRequestOptions(
            charging_enabled=True,
            first_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[1, 2, 3, 4, 5],
                time=dt.time(8, 0)
            )
        ),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "1",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [1, 2, 3, 4, 5],
                            "time": {"time": "0800", "timeSection": 0}
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": False,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 0
                        }
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [9],
                            "time": {"time": "1200", "timeSection": 0}
                        },
                        "reservChargeSet": False
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 0,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
    (
        "Enabled - Departure 1 - With climate - Without off peak charging",
        ScheduleChargingClimateRequestOptions(
            charging_enabled=True,
            first_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[1, 2, 3, 4, 5],
                time=dt.time(8, 0)
            ),
            climate_enabled=True,
            temperature=24.0,
        ),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "1",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [1, 2, 3, 4, 5],
                            "time": {"time": "0800", "timeSection": 0}
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": False,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 1
                        }
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [9],
                            "time": {"time": "1200", "timeSection": 0}
                        },
                        "reservChargeSet": False
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 0,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
    (
        "Enabled - Departure 1 & 2 - With climate - Without off peak charging",
        ScheduleChargingClimateRequestOptions(
            charging_enabled=True,
            first_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[1, 2, 3, 4, 5],
                time=dt.time(8, 0)
            ),
            second_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[0, 6],
                time=dt.time(12, 0)
            ),
            climate_enabled=True,
            temperature=24.0,
            defrost=True
        ),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "1",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [1, 2, 3, 4, 5],
                            "time": {"time": "0800", "timeSection": 0}
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": True,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 1
                        }
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [0, 6],
                            "time": {"time": "1200", "timeSection": 1} # FIXME: API reverse engineering always return a timeSection of 0 when asking for 12:** PM. Is that just a bug with the web app?
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": True,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 1
                        }
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 0,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
    (
        "Enabled - Departure 1 & 2 - With climate - With off peak charging (priority)",
        ScheduleChargingClimateRequestOptions(
            charging_enabled=True,
            first_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[1, 2, 3, 4, 5],
                time=dt.time(8, 0)
            ),
            second_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[0, 6],
                time=dt.time(12, 0)
            ),
            climate_enabled=True,
            temperature=24.0,
            defrost=True,
            heating=CLIMATE_HEATING_LEVEL.SIDE_MIRROR_REAR_WINDOW,
            off_peak_mode=OFF_PEAK_MODE.PRIORITY,
            off_peak_start_time=dt.time(20, 0),
            off_peak_end_time=dt.time(6, 0)
        ),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "1",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [1, 2, 3, 4, 5],
                            "time": {"time": "0800", "timeSection": 0}
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": True,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 1,
                            "heating1": 2
                        }
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [0, 6],
                            "time": {"time": "1200", "timeSection": 1} # FIXME: API reverse engineering always return a timeSection of 0 when asking for 12:** PM. Is that just a bug with the web app?
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": True,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 1
                        }
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 1,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "0800", "timeSection": 1},
                        "endtime": {"time": "0600", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
    (
        "Enabled - Departure 1 - With climate - With off peak charging (only)",
        ScheduleChargingClimateRequestOptions(
            charging_enabled=True,
            first_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[1, 2, 3, 4, 5],
                time=dt.time(8, 0)
            ),
            climate_enabled=True,
            temperature=24.0,
            defrost=True,
            heating=CLIMATE_HEATING_LEVEL.STEERING_WHEEL,
            off_peak_mode=OFF_PEAK_MODE.ONLY,
            off_peak_start_time=dt.time(20, 0),
            off_peak_end_time=dt.time(6, 0)
        ),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "1",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [1, 2, 3, 4, 5],
                            "time": {"time": "0800", "timeSection": 0}
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": True,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 1,
                            "heating1": 3
                        }
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [9],
                            "time": {"time": "1200", "timeSection": 0}
                        },
                        "reservChargeSet": False
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 2,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "0800", "timeSection": 1},
                        "endtime": {"time": "0600", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
    (
        "Backward Compatibility - Off peak charge only enabled",
        ScheduleChargingClimateRequestOptions(
            charging_enabled=True,
            first_departure=ScheduleChargingClimateRequestOptions.DepartureOptions(
                enabled=True,
                days=[1, 2, 3, 4, 5],
                time=dt.time(8, 0)
            ),
            climate_enabled=False,
            off_peak_charge_only_enabled=True,
            off_peak_start_time=dt.time(23, 0),
            off_peak_end_time=dt.time(7, 0)
        ),
        {
            "pin": "1234",
            "reservChargeInfos": {
                "reservFlag": "1",
                "reservChargeInfo": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [1, 2, 3, 4, 5],
                            "time": {"time": "0800", "timeSection": 0}
                        },
                        "reservChargeSet": True,
                        "reservFatcSet": {
                            "defrost": False,
                            "airTemp": {
                                "value": "14H",
                                "unit": 0,
                                "hvacTempType": 1
                            },
                            "airCtrl": 0
                        }
                    }
                },
                "reserveChargeInfo2": {
                    "reservChargeInfoDetail": {
                        "reservInfo": {
                            "day": [9],
                            "time": {"time": "1200", "timeSection": 0}
                        },
                        "reservChargeSet": False
                    }
                },
                "offpeakPowerInfo": {
                    "offPeakPowerFlag": 2,
                    "offPeakPowerTime1": {
                        "starttime": {"time": "1100", "timeSection": 1},
                        "endtime": {"time": "0700", "timeSection": 0}
                    },
                    "offPeakPowerTime2": {
                        "starttime": {"time": "0000", "timeSection": 0},
                        "endtime": {"time": "0100", "timeSection": 0}
                    }
                }
            }
        }
    ),
]

@patch('hyundai_kia_connect_api.KiaUvoApiCA.RetrySession')
@pytest.mark.parametrize("name, options, expected_payload", TEST_CASES)
def test_schedule_charging_and_climate(mock_session_cls, api, token, vehicle, name, options, expected_payload):
    # Mock the session and its post method
    mock_session = mock_session_cls.return_value
    api._sessions = mock_session

    # Mock response for _get_pin_token (vrfypin)
    mock_pin_response = MagicMock()
    mock_pin_response.json.return_value = {"result": {"pAuth": "test_p_auth"}}

    # Mock response for schedule request (evc/srcfs)
    mock_schedule_response = MagicMock()
    mock_schedule_response.headers = {"transactionId": "test_transaction_id"}
    mock_schedule_response.json.return_value = {"responseHeader": {"responseCode": 0}}

    # Configure side_effect to return different responses for sequential calls
    # 1. vrfypin
    # 2. evc/srcfs
    mock_session.post.side_effect = [mock_pin_response, mock_schedule_response]

    transaction_id = api.schedule_charging_and_climate(token, vehicle, options)

    assert transaction_id == "test_transaction_id"

    # Verify the payload sent to evc/srcfs
    # The second call to post is the schedule request (first was PIN)
    args, kwargs = mock_session.post.call_args_list[1]
    url = args[0]
    assert url.endswith("evc/srcfs")

    payload = json.loads(kwargs['data'])

    # Helper to compare dictionaries recursively
    def assert_dict_subset(expected, actual, path="root"):
        for key, value in expected.items():
            assert key in actual, f"Missing key {key} in {path}"
            if isinstance(value, dict):
                assert isinstance(actual[key], dict), f"Key {key} in {path} should be dict"
                assert_dict_subset(value, actual[key], path=f"{path}.{key}")
            else:
                assert actual[key] == value, f"Mismatch at {path}.{key}: expected {value}, got {actual[key]}"

    assert_dict_subset(expected_payload, payload)

@pytest.mark.parametrize("name, options, expected_payload", TEST_CASES)
def test_update_vehicle_properties_scheduled_charging(api, vehicle, name, options, expected_payload):
    state = expected_payload["reservChargeInfos"]
    api._update_vehicle_properties_scheduled_charging(vehicle, state)

    assert vehicle.ev_schedule_charge_enabled == bool(options.charging_enabled)

    # First Departure
    if options.first_departure and options.first_departure.enabled:
        assert vehicle.ev_first_departure_enabled is True
        if options.first_departure.days:
            assert vehicle.ev_first_departure_days == options.first_departure.days
        if options.first_departure.time:
            assert vehicle.ev_first_departure_time == options.first_departure.time

        assert vehicle.ev_first_departure_climate_enabled == bool(options.climate_enabled)
        assert vehicle.ev_first_departure_climate_defrost == bool(options.defrost)
        if options.heating is not None:
            assert vehicle.ev_first_departure_climate_heating == options.heating

        if options.temperature:
            assert vehicle.ev_first_departure_climate_temperature == options.temperature
    else:
        assert not vehicle.ev_first_departure_enabled

    # Off Peak
    if options.off_peak_mode is not None:
        assert vehicle.ev_off_peak_mode == options.off_peak_mode
    elif options.off_peak_charge_only_enabled:
        assert vehicle.ev_off_peak_mode == OFF_PEAK_MODE.ONLY
    else:
        assert vehicle.ev_off_peak_mode == OFF_PEAK_MODE.DISABLED

    if options.off_peak_start_time:
        assert vehicle.ev_off_peak_start_time == options.off_peak_start_time
    if options.off_peak_end_time:
        assert vehicle.ev_off_peak_end_time == options.off_peak_end_time
