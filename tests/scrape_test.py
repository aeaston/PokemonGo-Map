import scrape
from scrape import Location


def test_generate_location_steps():
    assert list(scrape.generate_location_steps4(Location(0, 0), 3)) == [
        Location(0.0, 0.0),
        Location(0.00135000135000135, 0.0),
        Location(0.000675000675000675, 0.0011691354642444562),
        Location(-0.000675000675000675, 0.0011691354642444562),
        Location(-0.00135000135000135, 0.0),
        Location(-0.000675000675000675, -0.0011691354642444562),
        Location(0.000675000675000675, -0.0011691354642444562),
        Location(0.002025002025002025, -0.0011691354642444562),
        Location(0.0027000027000027, 0.0),
        Location(0.002025002025002025, 0.0011691354642444562),
        Location(0.00135000135000135, 0.0023382709284889124),
        Location(0.0, 0.0023382709284889124),
        Location(-0.00135000135000135, 0.0023382709284889124),
        Location(-0.002025002025002025, 0.0011691354642444562),
        Location(-0.0027000027000027, 0.0),
        Location(-0.002025002025002025, -0.0011691354642444562),
        Location(-0.00135000135000135, -0.0023382709284889124),
        Location(0.0, -0.0023382709284889124),
        Location(0.00135000135000135, -0.0023382709284889124),
    ]
    assert list(scrape.generate_location_steps4(Location(50, 100), 3)) == [
        Location(50.0, 100.0),
        Location(50.00135000135, 100.0),
        Location(50.000675000675, 100.00181885270925),
        Location(49.999324999325, 100.00181885270925),
        Location(49.99864999865, 100.0),
        Location(49.999324999325, 99.99818114729075),
        Location(50.000675000675, 99.99818114729075),
        Location(50.002025002025, 99.99818114729075),
        Location(50.0027000027, 100.0),
        Location(50.002025002025, 100.00181885270925),
        Location(50.00135000135, 100.0036377054185),
        Location(50.0, 100.0036377054185),
        Location(49.99864999865, 100.0036377054185),
        Location(49.997974997975, 100.00181885270925),
        Location(49.9972999973, 100.0),
        Location(49.997974997975, 99.99818114729075),
        Location(49.99864999865, 99.9963622945815),
        Location(50.0, 99.9963622945815),
        Location(50.00135000135, 99.9963622945815),
    ]


def test_generate_location_steps2():
    assert list(scrape.generate_location_steps2(3)) == [
        (0, 0),
        (1, 0),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (0, -1),
        (1, -1),
        (2, -1),
        (2, 0),
        (1, 1),
        (0, 2),
        (-1, 2),
        (-2, 2),
        (-2, 1),
        (-2, 0),
        (-1, -1),
        (0, -2),
        (1, -2),
        (2, -2),
    ]


def test_generate_location_steps3():
    assert list(scrape.generate_location_steps3(3)) == [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.5, 0.8660254037844386),
        (-0.5, 0.8660254037844386),
        (-1.0, 0.0),
        (-0.5, -0.8660254037844386),
        (0.5, -0.8660254037844386),
        (1.5, -0.8660254037844386),
        (2.0, 0.0),
        (1.5, 0.8660254037844386),
        (1.0, 1.7320508075688772),
        (0.0, 1.7320508075688772),
        (-1.0, 1.7320508075688772),
        (-1.5, 0.8660254037844386),
        (-2.0, 0.0),
        (-1.5, -0.8660254037844386),
        (-1.0, -1.7320508075688772),
        (0.0, -1.7320508075688772),
        (1.0, -1.7320508075688772),
    ]
