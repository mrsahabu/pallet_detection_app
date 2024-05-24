import axios from "axios";

export default class ApiService {
  apiBaseURL = "http://0.0.0.0:8000/";

  getAccessToken() {
    const token = JSON.parse(localStorage.getItem("tokens"));
    if (token?.access_token) {
      return token?.access_token;
    } else {
      return false;
    }
  }

  getRefreshToken() {
    const token = JSON.parse(localStorage.getItem("tokens"));
    if (token?.refresh_token) {
      return token?.refresh_token;
    } else {
      return false;
    }
  }

  getAdmin() {
    const token = localStorage.getItem("admin");
    if (token?.refresh_token) {
      return token?.refresh_token;
    } else {
      return false;
    }
  }

  logIn = (payload) => {
    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
    };
    const encodeFormData = (payload) => {
      return Object.keys(payload)
        .map(
          (key) =>
            encodeURIComponent(key) + "=" + encodeURIComponent(payload[key])
        )
        .join("&");
    };
    return axios.post(this.apiBaseURL + "auth/token", encodeFormData(payload), {
      headers,
    });
  };

  logOut() {
    const headers = {
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    const refresh = this.getRefreshToken();
    return axios.post(
      this.apiBaseURL + "auth/logout/",
      { refresh },
      { headers }
    );
  }

  refreshToken() {
    const refresh = this.getRefreshToken();
    return axios.post(this.apiBaseURL + "auth/login/refresh/", { refresh });
  }

  registerUser(data) {
    return axios.post(this.apiBaseURL + "users/", data);
  }

  uploadImages(images) {
    const formData = new FormData();

    images.forEach((image, index) => {
      if (image.file && !image?.base64) {
        // If it's a file, append it directly
        formData.append(`files`, image.file);
      } else if (image.base64) {
        // If it's a base64 string, convert to Blob and append
        const base64Data = image.file.split(",")[1];
        const mimeType = image.file.match(/data:([^;]+);base64/)[1];
        debugger

        const byteString = atob(base64Data);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const uint8Array = new Uint8Array(arrayBuffer);

        for (let i = 0; i < byteString.length; i++) {
          uint8Array[i] = byteString.charCodeAt(i);
        }

        const blob = new Blob([arrayBuffer], { type: mimeType });
        formData.append("files", blob);
      }
    });

    const headers = {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    return axios.post(
      this.apiBaseURL +
        "pallet_detection/image_upload?email_to=st747809%40gmail.com",
      formData,
      { headers }
    );
  }

  getALLVideos() {
    const headers = {
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    return axios.post("users/get_all_videos_details", {}, { headers });
  }
}
