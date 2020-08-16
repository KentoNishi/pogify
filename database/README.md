## Database

This is a fully asyncronous publish and receive database which uses post requests to publish and sockets to access updates.
Examples of usage in js are in ``examples/``. 

## Goals

  - [x] real time
  - [ ] benchmark
  - [ ] convert pogify to use database
  - [ ] authentication

## Usage

Create a new firebase realtime database and set permissions to allow all reads and writes. Save the database url in ``database/personal.py`` as ``firebase_url = url``.
