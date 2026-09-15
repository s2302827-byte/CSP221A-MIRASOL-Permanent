import numpy as np
import pandas as pd


class InvalidScoreError(ValueError):
    
    def __init__(self, message: str, offending_score: Any):
        super().__init__(message)
        self.offending_score = offending_score

class StudentRecordLockedError(Exception):
    
    def __init__(self, message: str, student_name: str):
        super().__init__(message)
        self.student_name = student_name


class Student:
    def __init__(self, name: str, scores: Any):
        
        self.name: str = str(name)
        
       
        try:
            scores_arr = np.array(scores, dtype=float)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Could not convert scores to numeric array: {e}")
            
        if np.any((scores_arr < 0) | (scores_arr > 100)):
            raise InvalidScoreError("Scores must be between 0 and 100 inclusive.", scores)
            
        self._scores: np.ndarray = scores_arr
        self._locked: bool = False

    def lock(self) -> None:
        """Locks the student record to prevent future mutations."""
        self._locked = True

    def add_score(self, score: float) -> None:
        """Rule 2: Adds a score only if the record isn't locked and score is valid."""
        if self._locked:
            raise StudentRecordLockedError(f"Cannot add score. Record for '{self.name}' is locked.", self.name)
            
        try:
            val = float(score)
        except (ValueError, TypeError):
            raise InvalidScoreError(f"Score must be a valid number.", score)
            
        if val < 0 or val > 100:
            raise InvalidScoreError(f"Score must be between 0 and 100 inclusive.", val)
            
        self._scores = np.append(self._scores, val)

    def average(self) -> float:
        """Calculates the mean score using np.mean()."""
        if self._scores.size == 0:
            return 0.0
        return float(np.mean(self._scores))

   
    def __str__(self) -> str:
        return f"Student(Name: {self.name}, Average: {self.average():.2f})"

    def __repr__(self) -> str:
        return f"Student(name={repr(self.name)}, scores={repr(self._scores.tolist())})"


def process_student_data(raw_rows: List[Dict[str, Any]]) -> Tuple[List[Student], List[Dict[str, Any]]]:
    if not raw_rows:
        return [], []

    
    df = pd.DataFrame(raw_rows)
    df['original_dict'] = [row.copy() for row in raw_rows]
    
   
    df['name_clean'] = df['name'].astype(str).str.strip()
    df['scores_str'] = df['scores'].apply(lambda x: str(x))
    
   
    df = df.drop_duplicates(subset=['name_clean', 'scores_str'], keep='first')
    
    students: List[Student] = []
    failures: List[Dict[str, Any]] = []
    
   
    for _, row in df.iterrows():
        orig = row['original_dict']
        name_input = row['name']
        scores_input = row['scores']
        
        try:
           
            if isinstance(scores_input, str):
                parsed_scores = [float(x.strip()) for x in scores_input.split(',') if x.strip()]
            elif hasattr(scores_input, '__iter__'):
                parsed_scores = [float(x) for x in scores_input]
            else:
                parsed_scores = [float(scores_input)]
                
            
            student = Student(name_input, parsed_scores)
            students.append(student)
            
        except (ValueError, TypeError) as parse_err:
            failures.append({"row": orig, "error": f"Parse failure: {parse_err}"})
        except InvalidScoreError as val_err:
            failures.append({"row": orig, "error": f"Validation failure: {val_err}"})
            
    return students, failures


def rank_students(students: List[Student]) -> List[Student]:
    """Sorts students by average score in descending order using sorted() with a lambda key."""
    return sorted(students, key=lambda s: s.average(), reverse=True)



if __name__ == "__main__":
    
    raw_rows = [
    {"name": " Amara ", "scores": "92,85,78"},
    {"name": "Leo", "scores": "88,91,73"},
    {"name": "Priya", "scores": "65,72,150"},         
    {"name": "Sam", "scores": "70,not_a_number,60"},  
    {"name": "Amara", "scores": "95,90,88"},          
    {"name": "Jade", "scores": "81,77,84,90"},
    ]

    students_list, failed_list = process_student_data(raw_rows)
    
    demo = Student("Amara", [92,85,78])
    demo.lock()
    try:
        demo.add_score(90)
    except StudentRecordLockedError as e:
        print(e)

    ranked_list = rank_students(students_list)
    for idx, s in enumerate(ranked_list, 1):
        print(f"{idx}. {s.name} — {s.average():.2f} avg.")