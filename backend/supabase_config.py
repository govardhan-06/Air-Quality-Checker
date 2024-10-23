import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

class Supabase:
    def __init__(self):
        '''
        Initialize the Supabase client with your project's URL and key.
        '''
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client= create_client(self.url, self.key)

    def insert_item(self,data):
        '''
        Inserts the air quality_data into the Supabase table.
        '''
        response = self.client.table("quality_data").insert(data).execute()
        if response:
            print(f"Inserted successfully!")
        else:
            print(f"Failed to insert : {response.text}")
    
    def fetch_item(self, count: int):
        '''
        Fetches items from the Supabase table.
        '''
        try:
            response = self.client.table("quality_data").select("*").limit(count).execute()
            if response:
                return response.data  

        except Exception as e:
            print(f"An exception occurred: {e}")  
            return []  

if __name__ == "__main__":
    supabase_client = Supabase()
    
    # Data for module testing
    test_data = {
            "sensor_id": "1001",
            "location": "VIT CHENNAI",
            "co2_level": 23.32,
            "pm25_level": 32.65,
            "no2_level": 12.65
    }

    supabase_client.insert_item(test_data)

    fetched_data = supabase_client.fetch_item(30)
    
    print("Fetched data:")
    print(fetched_data)
