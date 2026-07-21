import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
django.setup()

from apps.core.models import Place

rich_data = {
    "Hawa Mahal": {
        "desc": "The Hawa Mahal, or 'Palace of Winds', is an iconic five-story palace built from red and pink sandstone in the heart of Jaipur. Its unique exterior is akin to the honeycomb of a beehive with its 953 small windows called Jharokhas decorated with intricate latticework.",
        "hist": "Built in 1799 by Maharaja Sawai Pratap Singh, the grandson of Maharaja Sawai Jai Singh, who was the founder of Jaipur. It was designed by Lal Chand Ustad. The original intent of the lattice design was to allow royal ladies to observe everyday life and festivals celebrated in the street below without being seen.",
        "year": "1799",
        "amenities": {"parking_available": "Yes", "guided_tours": "Yes", "photography_allowed": "Yes", "audio_guide": "Yes"}
    },
    "India Gate": {
        "desc": "The India Gate (formerly known as the All India War Memorial) is a war memorial located astride the Rajpath, on the eastern edge of the ceremonial axis of New Delhi. It stands as a majestic archway and a symbol of sacrifice.",
        "hist": "Designed by Sir Edwin Lutyens, the India Gate commemorates the 70,000 soldiers of the British Indian Army who died between 1914 and 1921 in the First World War. Following the Bangladesh Liberation war in 1972, a structure consisting of a black marble plinth with a reversed rifle, capped by a war helmet, bounded by four eternal flames, was built beneath the arch. This structure, called Amar Jawan Jyoti, served as India's Tomb of the Unknown Soldier.",
        "year": "1931",
        "amenities": {"parking_available": "Yes", "wheelchair_accessible": "Yes", "photography_allowed": "Yes"}
    },
    "Lotus Temple": {
        "desc": "The Lotus Temple, located in Delhi, is a Bahá'í House of Worship notable for its flowerlike shape. It has become a prominent attraction in the city, serving as a tranquil haven that welcomes people of all religions to pray or meditate.",
        "hist": "Designed by Iranian architect Fariborz Sahba, the temple was dedicated in December 1986. Like all Bahá'í Houses of Worship, the Lotus Temple is open to all, regardless of religion or any other qualification. It is composed of 27 free-standing marble-clad 'petals' arranged in clusters of three to form nine sides.",
        "year": "1986",
        "amenities": {"parking_available": "Yes", "wheelchair_accessible": "Yes", "guided_tours": "Yes", "photography_allowed": "Yes"}
    },
    "Akshardham Temple": {
        "desc": "Swaminarayan Akshardham is a massive Hindu temple complex in Delhi that displays millennia of traditional Indian and Hindu culture, spirituality, and architecture. It features a stunning central monument crafted entirely of stone without any structural steel.",
        "hist": "The complex was officially opened on 6 November 2005 by Dr. A.P.J. Abdul Kalam. It was constructed by the BAPS organization under the inspiration of Pramukh Swami Maharaj. It showcases the life and work of Swaminarayan and classical Indian arts through breathtaking exhibitions and boat rides.",
        "year": "2005",
        "amenities": {"parking_available": "Yes", "wheelchair_accessible": "Yes", "audio_guide": "Yes", "guided_tours": "Yes"}
    },
    "Vivekananda Rock Memorial": {
        "desc": "Vivekananda Rock Memorial is a monument and popular tourist monument in Kanyakumari, India's southernmost tip. It stands on one of two rocks located about 500 meters off the mainland, marking the meeting point of the Bay of Bengal, the Arabian Sea, and the Indian Ocean.",
        "hist": "Built in 1970 in honor of Swami Vivekananda, who is said to have attained enlightenment on the rock. It was spearheaded by Eknath Ranade and involved immense effort from across the nation to construct this grand symbol of Indian spirituality and architectural brilliance.",
        "year": "1970",
        "amenities": {"wheelchair_accessible": "No", "guided_tours": "Yes", "photography_allowed": "Yes"}
    },
    "Gol Gumbaz": {
        "desc": "Gol Gumbaz is the magnificent mausoleum of King Mohammed Adil Shah, Sultan of Bijapur. Known for its staggering dimensions, the structure boasts one of the largest domes in the world, renowned for its incredible acoustic properties.",
        "hist": "Construction of the tomb was started in 1626 and completed in 1656. The name is based on Gol Gumbadh derived from Gol Gumbaz meaning 'circular dome'. The dome is famous for its 'Whispering Gallery' where even the softest sound can be heard clearly on the other side.",
        "year": "1656",
        "amenities": {"parking_available": "Yes", "photography_allowed": "Yes", "guided_tours": "Yes"}
    },
    "Kumbhalgarh Fort": {
        "desc": "Kumbhalgarh Fort is a formidable Mewar fortress on the westerly range of Aravalli Hills. It is famous for its massive wall, which stretches for 36 kilometers, making it the second-longest continuous wall in the world after the Great Wall of China.",
        "hist": "Built during the course of the 15th century by Rana Kumbha, the fort remained unconquered due to its strategic and inaccessible location. It is also the birthplace of Maharana Pratap, the great king and warrior of Mewar. It was declared a UNESCO World Heritage Site in 2013.",
        "year": "15th Century",
        "amenities": {"parking_available": "Yes", "guided_tours": "Yes", "photography_allowed": "Yes"}
    },
    "Chittorgarh Fort": {
        "desc": "Chittorgarh Fort is one of the largest forts in India and Asia. It sprawls majestically over a hill above the plains of the valley drained by the Berach River. A symbol of Rajput prowess and pride, the fort complex houses numerous historical palaces, gates, and temples.",
        "hist": "Historically, it was the capital of Mewar and is today situated in the Chittorgarh city. The fort has seen several sieges, most notably by Alauddin Khalji in 1303, Bahadur Shah of Gujarat in 1535, and Akbar in 1568. It is deeply associated with legendary figures like Rani Padmini and the mystic poet Meera Bai.",
        "year": "7th Century",
        "amenities": {"parking_available": "Yes", "guided_tours": "Yes", "photography_allowed": "Yes"}
    },
    "Somnath Temple": {
        "desc": "The Somnath temple located in Prabhas Patan near Veraval in Saurashtra is a highly revered pilgrimage site. It is believed to be the first among the twelve Jyotirlinga shrines of Shiva, standing majestically right on the shores of the Arabian Sea.",
        "hist": "The temple has a tumultuous history, having been reconstructed several times in the past after repeated destruction by various Muslim invaders, most notably Mahmud of Ghazni in 1024. The present temple was reconstructed in the Chaulukya style of Hindu temple architecture and completed in May 1951.",
        "year": "1951 (Rebuilt)",
        "amenities": {"parking_available": "Yes", "wheelchair_accessible": "Yes", "photography_allowed": "No"}
    },
    "Howrah Bridge": {
        "desc": "The Howrah Bridge is a balanced cantilever bridge over the Hooghly River in West Bengal. It connects the twin cities of Howrah and Kolkata and is one of the most iconic landmarks of the region, carrying over 100,000 vehicles and 150,000 pedestrians daily.",
        "hist": "Commissioned in 1943, it was originally named the New Howrah Bridge because it replaced a pontoon bridge at the same location. It was constructed without the use of nuts and bolts, being formed entirely by riveting. It was renamed Rabindra Setu in 1965 after the great Bengali poet Rabindranath Tagore.",
        "year": "1943",
        "amenities": {"parking_available": "No", "photography_allowed": "Yes"}
    },
    "Badrinath Temple": {
        "desc": "Badrinath Temple is a highly revered Hindu temple dedicated to Lord Vishnu, situated in the town of Badrinath in Uttarakhand. Flanked by the Nar and Narayana mountain ranges, it is one of the pivotal Char Dham pilgrimage sites.",
        "hist": "The temple finds mention in several ancient Hindu texts. It is believed to have been established by Adi Shankaracharya in the 8th century. The current structure was built by the Kings of Garhwal. Due to extreme weather conditions in the Himalayan region, the temple is open only for six months every year.",
        "year": "8th Century",
        "amenities": {"parking_available": "No", "wheelchair_accessible": "No", "photography_allowed": "No"}
    },
    "Kedarnath Temple": {
        "desc": "Kedarnath Temple is one of the most sacred Hindu temples dedicated to Lord Shiva, located in the Garhwal Himalayan range near the Mandakini river. It is one of the twelve Jyotirlingas and the highest among the 12 Jyotirlingas.",
        "hist": "The temple is believed to have been originally built by the Pandavas of the Mahabharata epic and later revived by Adi Shankara in the 8th century CE. It has survived harsh centuries of extreme weather, including being buried in snow for around 400 years during the Little Ice Age, and stood resilient during the 2013 flash floods.",
        "year": "8th Century",
        "amenities": {"parking_available": "No", "wheelchair_accessible": "No", "photography_allowed": "No"}
    }
}

updated_count = 0
for name, data in rich_data.items():
    try:
        place = Place.objects.get(place_name=name)
        place.description = data["desc"]
        place.history = data["hist"]
        place.year_established = data["year"]
        
        # Amenities
        amenities = data.get("amenities", {})
        if "parking_available" in amenities: place.parking_available = amenities["parking_available"]
        if "wheelchair_accessible" in amenities: place.wheelchair_accessible = amenities["wheelchair_accessible"]
        if "guided_tours" in amenities: place.guided_tours = amenities["guided_tours"]
        if "audio_guide" in amenities: place.audio_guide = amenities["audio_guide"]
        if "photography_allowed" in amenities: place.photography_allowed = amenities["photography_allowed"]
        
        place.save()
        print(f"Enriched {name}")
        updated_count += 1
    except Place.DoesNotExist:
        print(f"Could not find {name}")

print(f"Successfully enriched {updated_count} places.")
