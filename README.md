# tracker
Track your devices at a glance with total ownership of your data; a FOSS, self-hosted alternative to Apple's Find My.

## Installation

You'll need Python installed to run the server.

First, clone the repository:

```bash
git clone https://github.com/eskaliert680/tracker.git
cd tracker
```

### Set up location daemon
You need this to continuously update the location of your device.

### Set up server
Install dependencies

```bash
cd server
pip install -r dependencies.txt
```

add a `.env` file

```bash
mv .env.example .env
```

Now you'll need to set up a Supabase project.
