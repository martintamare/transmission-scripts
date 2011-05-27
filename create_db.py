#! /usr/bin/env python2.6
import sqlite3

# Connect sqlite
conn = sqlite3.connect('/home/torrent/transmission-scripts/rss.db')
c = conn.cursor()

# Create table
c.execute("create table rss_info(filename text, date text, info text, path text)")

# Save (commit) the changes
conn.commit()

# We can also close the cursor if we are done with it
c.close()