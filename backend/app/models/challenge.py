class Challenge: 
    def __init__(self, pk, sk, id, title, description, difficulty, category, points, completion_rate, created_at, updated_at, tags):
        self.pk = pk
        self.sk = str(sk)  # Ensure sk is a string
        self.id = str(id)  # Ensure id is a string
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.category = category
        self.points = points
        self.completion_rate = completion_rate
        self.created_at = created_at
        self.updated_at = updated_at
        self.tags = tags
    
    def __repr__(self):
        return f"<Challenge {self.id}>"
    
    def to_dict(self):
        return {
            "pk": self.pk,
            "sk": self.sk,  
            "id": self.id,  
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "category": self.category,
            "points": self.points,
            "completion_rate": self.completion_rate,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags
        }
        
    @staticmethod
    def from_dict(data):
        return Challenge(
            data.get("pk"),
            str(data.get("sk")),  
            str(data.get("id")),
            data.get("title"),
            data.get("description"),
            data.get("difficulty"),
            data.get("category"),
            data.get("points"),
            data.get("completion_rate"),
            data.get("created_at"),
            data.get("updated_at"),
            data.get("tags")
        )
    
    @staticmethod
    def from_db(data):
        return Challenge(
            data.get("pk"),
            str(data.get("sk")),
            str(data.get("id")), 
            data.get("title"),
            data.get("description"),
            data.get("difficulty"),
            data.get("category"),
            data.get("points"),
            data.get("completion_rate"),
            data.get("created_at"),
            data.get("updated_at"),
            data.get("tags")
        )
