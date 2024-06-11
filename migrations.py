# migrations.py is for building your database

async def m001_initial(db):
   await db.execute(
       f"""
       CREATE TABLE mysuperplugin.payment (
           payment_id TEXT
       );
   """
   )
