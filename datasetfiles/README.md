# HeritageHub Dataset — Phase 1

## What's in this delivery

- `schema.sql` — full MySQL schema, 3NF normalized, with PKs, FKs, and indexes.
- `states.csv` — all 28 states + 8 union territories (36 rows).
- `districts.csv`, `cities.csv` — derived from the places below.
- `categories.csv` — all 43 categories you listed.
- `places.csv` — **107 real, verifiable major heritage/tourism sites**, covering
  every state and union territory (at least 2–5 flagship sites each): UNESCO
  sites, ASI-protected monuments, major forts, palaces, temples, national
  parks, tiger reserves, etc.
- `place_images.csv`, `ticket_prices.csv`, `events.csv` — linked child tables.
- `reviews.csv` — synthetic sample reviews (clearly marked, not real user data).
- `users.csv`, `bookings.csv`, `wishlists.csv`, `notifications.csv` — synthetic
  sample data for app testing, as you requested.

## Why 107 rows, not 5,000–10,000

I want to be upfront about this rather than pad the file with lower-quality
entries: **India has roughly 3,600 ASI-protected monuments in total**, plus a
few hundred additional UNESCO/national-park/major-museum sites. To reach
5,000–10,000 *real, non-duplicated* places I would need to include very minor
local shrines, small unlisted step wells, etc. — most of which have **no
public, verifiable data** for fields like exact contact numbers, emails,
ratings, or review counts. Filling those in would mean inventing data that
looks real but isn't, which defeats the "verified" and "no dummy data"
requirements you specified.

## What's honest vs. what's marked

For every one of the 107 places:
- Name, state/UT, district, city, category, coordinates, UNESCO status, ASI
  status, and the core historical fact are all real and drawn from
  well-documented public knowledge (UNESCO listings, ASI records, standard
  tourism references).
- Fields that are **not reliably public per-site** (exact phone number,
  email, nearest airport/station by name, official website URL, exact
  pincode, altitude, image URLs) are explicitly marked `NULL - verify ...`
  rather than fabricated. This is intentional — please enrich these via a
  live source (Google Places API, ASI/state tourism portals) before
  production use.
- `rating` and `number_of_reviews` are **plausibly realistic placeholder
  values**, not scraped real ratings — flag these for the same reason.
- `users.csv`, `bookings.csv`, `wishlists.csv`, `notifications.csv`,
  `reviews.csv` are 100% synthetic sample/test data, as requested.

## Extending this dataset

This is Phase 1 (major flagship sites). I can continue in batches — e.g.
expand each state to include its full list of ASI-protected monuments,
secondary museums, wildlife sanctuaries, waterfalls, etc. — while keeping the
same honesty standard (real places only, unverifiable fields marked, not
invented). Tell me which states/categories to prioritize next and I'll keep
building.

## Import order (MySQL / Django)

```
states → districts → cities → categories → places →
place_images → ticket_prices → events → users → reviews →
bookings → wishlists → notifications
```
