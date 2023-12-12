import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    Reservation,
    ShowSession,
    Ticket,
)


class PlanetariumDomeTest(TestCase):
    def test_capacity_calculation(self):
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=5, seats_in_row=10)
        self.assertEqual(dome.capacity, 50)


class ShowThemeTest(TestCase):
    def test_str_representation(self):
        theme = ShowTheme.objects.create(name="Test Theme")
        self.assertEqual(str(theme), "Test Theme")


class AstronomyShowTest(TestCase):
    def test_str_representation(self):
        show = AstronomyShow.objects.create(title="Test Show", description="Test Description")
        self.assertEqual(str(show), "Test Show")


class ReservationTest(TestCase):
    def test_str_representation(self):
        user = get_user_model().objects.create_user(username="test", password="123321")
        reservation = Reservation.objects.create(user=user)
        self.assertEqual(
            str(reservation),
            f"Reservation by {user.username} created at {reservation.created_at}",
        )


class ShowSessionTest(TestCase):
    def setUp(self):
        self.dome = PlanetariumDome.objects.create(name="Test Dome", rows=5, seats_in_row=10)
        self.theme = ShowTheme.objects.create(name="Test Theme")
        self.show = AstronomyShow.objects.create(title="Test Show", description="Test Description")
        self.session = ShowSession.objects.create(
            astronomy_show=self.show, planetarium_dome=self.dome, show_time="2023-12-31 12:00:00+00:00"
        )

    def test_tickets_available_calculation(self):
        user = get_user_model().objects.create_user(username="test", password="123321")
        reservation = Reservation.objects.create(user=user, created_at=datetime.datetime.now())
        Ticket.objects.create(row=1, seat=1, show_session=self.session, reservation=reservation)
        self.assertEqual(self.session.tickets_available, self.dome.capacity - 1)

    def test_str_representation(self):
        self.assertEqual(
            str(self.session),
            f"Show: {self.show.title} In {self.dome.name} At 2023-12-31 12:00:00+00:00",
        )


class TicketTest(TestCase):
    def setUp(self):
        self.dome = PlanetariumDome.objects.create(name="Test Dome", rows=5, seats_in_row=10)
        self.theme = ShowTheme.objects.create(name="Test Theme")
        self.show = AstronomyShow.objects.create(title="Test Show", description="Test Description")
        self.session = ShowSession.objects.create(
            astronomy_show=self.show, planetarium_dome=self.dome, show_time="2023-12-31T12:00:00Z"
        )
        self.user = get_user_model().objects.create_user(username="test_user", password="test_password")

    def test_validate_ticket_success(self):
        Ticket.validate_ticket(row=1, seat=1, planetarium_dome=self.dome, error_to_raise=ValidationError)

    def test_validate_ticket_row_out_of_range(self):
        with self.assertRaises(ValidationError) as context:
            Ticket.validate_ticket(row=0, seat=1, planetarium_dome=self.dome, error_to_raise=ValidationError)
        self.assertIn("row number must be in available range", str(context.exception))

    def test_validate_ticket_seat_out_of_range(self):
        with self.assertRaises(ValidationError) as context:
            Ticket.validate_ticket(row=1, seat=15, planetarium_dome=self.dome, error_to_raise=ValidationError)
        self.assertIn("seat number must be in available range", str(context.exception))

    def test_clean_method(self):
        ticket = Ticket(row=1, seat=1, show_session=self.session, reservation=None)
        ticket.clean()

    def test_clean_method_invalid_ticket(self):
        ticket = Ticket(row=0, seat=1, show_session=self.session, reservation=None)
        with self.assertRaises(ValidationError) as context:
            ticket.clean()
        self.assertIn("row number must be in available range", str(context.exception))

    def test_str_representation(self):
        ticket = Ticket(row=1, seat=1, show_session=self.session, reservation=None)
        self.assertEqual(
            str(ticket),
            f"{str(self.session)} (row: {ticket.row}, seat: {ticket.seat})",
        )
