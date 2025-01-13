import json
import math

class KnowledgeBaseSystem:
    def __init__(self, json_file):
        self.json_file = json_file
        self.diseases_data = self.load_data()

    def load_data(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.json_file} không tồn tại.")
        except Exception as e:
            raise Exception(f"Lỗi khi đọc dữ liệu: {str(e)}")

    def cosine_similarity(self, vec1, vec2):
        """
        Tính toán cosine similarity giữa hai vector.
        vec1, vec2 là các vector đại diện cho các triệu chứng của bệnh và triệu chứng người dùng.
        """
        dot_product = sum([vec1[i] * vec2[i] for i in range(len(vec1))])
        norm_vec1 = math.sqrt(sum([v**2 for v in vec1]))
        norm_vec2 = math.sqrt(sum([v**2 for v in vec2]))
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0
        return dot_product / (norm_vec1 * norm_vec2)

    def build_feature_vector(self, symptoms, all_symptoms):
        """
        Xây dựng vector tính toán cho triệu chứng của bệnh và triệu chứng người dùng.
        """
        feature_vector = [0] * len(all_symptoms)
        for symptom in symptoms:
            if symptom.lower() in all_symptoms:
                feature_vector[all_symptoms.index(symptom.lower())] = 1
        return feature_vector

    def find_best_match(self, symptoms):
        all_symptoms = []
        # Tạo một danh sách tất cả các triệu chứng từ dữ liệu bệnh để làm cơ sở so sánh
        for disease in self.diseases_data:
            all_symptoms.extend([s.lower() for s in disease.get("symptoms", [])])

        # Loại bỏ các triệu chứng trùng lặp
        all_symptoms = list(set(all_symptoms))

        best_match_disease = None
        best_match_score = -1  # Điểm tương đồng cao nhất
        for disease in self.diseases_data:
            disease_symptoms = disease.get("symptoms", [])
            # Xây dựng vector cho triệu chứng của bệnh và triệu chứng người dùng
            user_vector = self.build_feature_vector(symptoms, all_symptoms)
            disease_vector = self.build_feature_vector(disease_symptoms, all_symptoms)

            # Tính toán điểm cosine similarity
            similarity_score = self.cosine_similarity(user_vector, disease_vector)

            if similarity_score > best_match_score:
                best_match_score = similarity_score
                best_match_disease = disease

        if best_match_disease:
            # Kiểm tra nếu không có trường 'how_to_care', gán giá trị mặc định
            how_to_care = best_match_disease.get("how_to_care", ["Không có hướng dẫn chăm sóc"])
            
            # Đảm bảo "how_to_care" là một danh sách
            if isinstance(how_to_care, str):
                how_to_care = [how_to_care]

            return [{
                "name": best_match_disease["name"],
                "info": best_match_disease.get("info", "Không có thông tin bệnh"),
                "path": best_match_disease.get("path", ""),
                "how_to_care": how_to_care,  # Trả về danh sách hướng dẫn chăm sóc
            }]
        else:
            return [{"message": "Không tìm thấy bệnh phù hợp", "diseases": []}]
