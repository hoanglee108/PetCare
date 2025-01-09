from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Knowledge_base_system import KnowledgeBaseSystem  # Import KnowledgeBaseSystem
import os
import json

app = Flask(__name__)
CORS(app)

# Thư mục chứa ảnh tĩnh
IMAGE_FOLDER = ''

# API phục vụ ảnh
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# API để xử lý dữ liệu từ React
@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.json
    select = data.get("select")
    symptoms = data.get("listInput")

    if select == "Dog":
        json_file = r"C:\Users\Admin\Desktop\codes\hcstt\AppPetCare\src\Dog24-12_modified.json"
    elif select == "Cat":
        json_file = r"C:\Users\Admin\Desktop\codes\hcstt\AppPetCare\src\Cat24-12_updated.json"
    elif select == "Hamster":
        json_file = r"C:\Users\Admin\Desktop\codes\hcstt\AppPetCare\src\Hamster24-12_modified.json"
    else:
        return jsonify({"message": "Không hỗ trợ loại thú cưng này", "diseases": []})

    # Sử dụng KnowledgeBaseSystem để tìm kiếm bệnh
    try:
        knowledge_base = KnowledgeBaseSystem(json_file)
        diseases = knowledge_base.find_best_match(symptoms)
        return jsonify({
            "message": "Dữ liệu xử lý thành công",
            "diseases": diseases
        })
    except Exception as e:
        return jsonify({"message": f"Lỗi: {str(e)}", "diseases": []})

@app.route('/get-symptoms', methods=['POST'])
def get_symptoms():
    try:
        data = request.json
        pet_type = data.get("select")

        # Map loại thú cưng đến file JSON tương ứng
        pet_files = {
            "Dog": r"C:\Users\Admin\Desktop\codes\hcstt\AppPetCare\src\Dog24-12_modified.json",
            "Cat": r"C:\Users\Admin\Desktop\codes\hcstt\AppPetCare\src\Cat24-12_updated.json",
            "Hamster": r"C:\Users\Admin\Desktop\codes\hcstt\AppPetCare\src\Hamster24-12_modified.json",
        }

        # Kiểm tra file tương ứng
        file_path = pet_files.get(pet_type)
        if not file_path:
            return jsonify({"error": "Loại thú cưng không hợp lệ"}), 400

        # Đọc triệu chứng từ file JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            symptoms = set()
            for disease in data:
                symptoms.update([s.lower() for s in disease["symptoms"]])

        return jsonify({"symptoms": sorted(list(symptoms))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
