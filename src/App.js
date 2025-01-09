import React, { useState, useEffect } from "react";
import "./App.css";
import dogCat from "./dogcat.webp";
import SelectSearch from "react-select-search";
import "react-select-search/style.css";
import Form from "react-bootstrap/Form";
import { processData } from './service';

function App() {
  const [listInput, setListInput] = useState(["", ""]);
  const [listError, setListError] = useState(["", ""]);
  const [select, setSelect] = useState("");
  const [selectError, setSelectError] = useState("");
  const [error, setError] = useState("");
  const [diseases, setDiseases] = useState([]);
  const [allSymptoms, setAllSymptoms] = useState([]); // Triệu chứng từ file JSON

  const baseURL = "http://localhost:5000/images/";

  // Gọi API để lấy danh sách triệu chứng khi thay đổi loại thú cưng
  useEffect(() => {
    if (select) {
      fetchSymptoms(select);
    }
  }, [select]);

  const fetchSymptoms = async (petType) => {
    try {
      const response = await fetch("http://localhost:5000/get-symptoms", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ select: petType }),
      });
      const data = await response.json();
      if (data.symptoms) {
        setAllSymptoms(data.symptoms);
      } else {
        console.error("Không thể tải triệu chứng:", data.error || "Unknown error");
        setAllSymptoms([]);
      }
    } catch (error) {
      console.error("Lỗi khi tải triệu chứng:", error);
      setAllSymptoms([]);
    }
  };

  const handleAddInput = () => {
    setError("");
    setListInput([...listInput, ""]);
    setListError([...listError, ""]);
  };

  const handleDeleteInput = () => {
    if (listInput.length <= 2) {
      setError("Cần ít nhất 2 triệu chứng!");
      return;
    }
    setError("");
    setListInput(listInput.slice(0, -1));
    setListError(listError.slice(0, -1));
  };

  const handleSymptomChange = (value, index) => {
    const updatedList = [...listInput];
    updatedList[index] = value;
    setListInput(updatedList);
  };

  const handleSelectChange = (value) => {
    setSelect(value);
    if (value.trim() !== "") {
      setSelectError("");
    }
  };

  const handleSubmit = async () => {
    const updatedErrors = [...listError];
    let hasError = false;

    listInput.forEach((item, index) => {
      if (item.trim() === "") {
        updatedErrors[index] = "Triệu chứng không được để trống";
        hasError = true;
      }
    });

    setListError(updatedErrors);

    if (select.trim() === "") {
      setSelectError("Vui lòng chọn loại thú cưng");
      hasError = true;
    }

    if (!hasError) {
      try {
        const response = await processData(select, listInput);
        setDiseases(response.diseases);
      } catch (error) {
        console.error("Lỗi khi xử lý dữ liệu:", error);
      }
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="introduction">
          <div className="text">
            <div className="text-child">Chuẩn đoán bệnh</div>
            <div className="text-child">Thú cưng</div>
          </div>
          <img src={dogCat} alt="img" className="dogCat" />
        </div>
        <div className="action">
          <div className="col-6 option">
            <Form.Select
              aria-label="Default select example"
              className="list-option"
              value={select}
              onChange={(e) => handleSelectChange(e.target.value)}
            >
              <option value="">Chọn loại thú cưng</option>
              <option value="Dog">Chó</option>
              <option value="Cat">Mèo</option>
              <option value="Hamster">Chuột hamster</option>
            </Form.Select>
            {selectError && <div className="text-danger">{selectError}</div>}
            <hr />

            {listInput.map((item, index) => (
              <div key={index} className="mb-3">
                <label>{`Triệu chứng ${index + 1}`}</label>
                <SelectSearch
                  options={allSymptoms.map((symptom) => ({
                    name: symptom,
                    value: symptom,
                  }))}
                  value={item}
                  search
                  placeholder={`Triệu chứng ${index + 1}`}
                  onChange={(value) => handleSymptomChange(value, index)}
                />
                {listError[index] && (
                  <div className="text-danger">{listError[index]}</div>
                )}
              </div>
            ))}
            {error && <div className="error text-danger">{error}</div>}

            <div className="list-button">
              <button className="btn btn-them" onClick={handleAddInput}>
                Thêm triệu chứng
              </button>
              <button
                className="btn btn-xoa"
                onClick={handleDeleteInput}
                disabled={listInput.length === 0}
              >
                Xóa triệu chứng
              </button>
              <button className="btn btn-confirm" onClick={handleSubmit}>
                Xác nhận
              </button>
            </div>
          </div>
          <div className="col-6 info">
            <div className="info-child">
              <div className="title">
                {diseases.length > 0
                  ? diseases.map((disease) => disease.name).join(", ")
                  : "Tên bệnh"}
              </div>
              <div className="description">
                {diseases.length > 0
                  ? diseases.map((disease, index) => (
                    <div key={index}>
                      <p>{disease.info}</p>
                      {disease.path && (
                        <img
                          src={`http://localhost:5000/images/${disease.path}`}
                          alt={`Image for ${disease.name}`}
                          className="disease-image"
                        />
                      )}
                    </div>
                  ))
                  : "Thông tin bệnh"}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
