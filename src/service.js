// Define the API service function
export const processData = async (select, listInput) => {
    try {
      // Define the API URL
      const apiUrl = 'http://127.0.0.1:5000/process-data';
  
      // Prepare the payload
      const payload = {
        select: select,
        listInput: listInput,
      };
  
      // Make the POST request
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      // Parse and return the JSON response
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      return data;
  
    } catch (error) {
      console.error('Error calling processData API:', error);
      throw error;
    }
  };
  