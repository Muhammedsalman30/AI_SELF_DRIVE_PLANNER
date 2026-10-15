# European Self-Drive Planner — Starter Dataset

This starter dataset is curated for the AI Self-Drive Tour Planner project.

## Contents
- countries.csv — 8 European countries
- destinations.csv — 19 cities/towns with approximate city-centre coordinates
- attractions.csv — 40 curated attractions linked to destination IDs
- route_templates.csv — 2 example circular route templates
- travel.db — pre-populated SQLite database with foreign keys and a circular-route check

## Strict dataset-only rule
The application should select destinations and attractions ONLY from these database tables.
Do not call an AI model, web search, Google Places, or another discovery service to add new places.
Google Maps is only for road distance, estimated driving time, and displaying a route between dataset-selected locations.

## Coordinate and route warning
Coordinates are approximate reference points for development, not surveyed navigation coordinates.
Before production use, validate each point in Google Maps. Google Maps should calculate road routes; do not calculate driving distance from straight-line coordinates.
The sample route templates are starting examples, not guaranteed practical itineraries. In particular, the Alpine/Italy route is long and needs a realistic trip duration, toll and border checks.

## Hotel data
No hotel inventory or hotel prices are included. Booking.com, Agoda and Expedia results must come from authorized partner/API access or clearly labelled test fixtures. Never present sample hotel prices as live or bookable.

## Suggested database loading
The travel.db file is already populated. In Python:
    import sqlite3
    conn = sqlite3.connect("data/travel.db")
    countries = pd.read_sql_query("SELECT * FROM countries", conn)

## Suggested future fields
For production, add source_url, source_name, last_verified_at, opening_hours, seasonal_notes, accessibility, and data_license fields for attraction records.
