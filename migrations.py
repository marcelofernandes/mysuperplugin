# migrations.py is for building your database

async def m001_initial(db):
   await db.execute(
       f"""
       CREATE TABLE mysuperplugin.payment (
           id TEXT PRIMARY KEY,
           payment_id TEXT NOT NULL,
           time TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
       );
   """
   )
