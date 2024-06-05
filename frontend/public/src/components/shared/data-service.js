import axios from "axios";

export default class ApiService {
  apiBaseURL = "https://srv531488.hstgr.cloud/";

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
    const admin = localStorage.getItem("admin");
    if (admin) {
      return !!admin;
    } else {
      return false;
    }
  }

  getUserDetails() {
    const headers = {
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    return axios.get(this.apiBaseURL + "users/me", { headers });
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
      this.apiBaseURL + "auth/logout",
      { refresh },
      { headers }
    );
  }

  forgetPassword(email) {
    return axios.post(
      this.apiBaseURL + `users/forgot_password?user_email=${email}`,
      {}
    );
  }

  resetPassword(password, token) {
    return axios.post(
      this.apiBaseURL +
        `users/reset_password?new_password=${password}&access_token=${token}`,
      {}
    );
  }
  refreshToken() {
    const refresh = this.getRefreshToken();
    return axios.post(this.apiBaseURL + "auth/login/refresh/", { refresh });
  }

  registerUser(data) {
    return axios.post(this.apiBaseURL + "users/create-user", data);
  }

  uploadImages(images, buy_or_sell) {
    const formData = new FormData();
    const files = [];

    images.forEach((image, index) => {
      if (image.file && !image?.base64) {
        // If it's a file, append it directly
        files.push(image.file);
      } else if (image.base64) {
        // If it's a base64 string, convert to Blob and append
        const base64Data = image.file.split(",")[1];
        const mimeType = image.file.match(/data:([^;]+);base64/)[1];
        const byteString = atob(base64Data);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const uint8Array = new Uint8Array(arrayBuffer);

        for (let i = 0; i < byteString.length; i++) {
          uint8Array[i] = byteString.charCodeAt(i);
        }

        const blob = new Blob([arrayBuffer], { type: mimeType });
        files.push(blob);
      }
    });
    files.forEach((file, index) => {
      formData.append(`files`, file);
    });

    formData.append("buy_or_sell", buy_or_sell);

    const headers = {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    return axios.post(this.apiBaseURL + `pallet_detection/upload`, formData, {
      headers,
    });
  }

  getALLUsersImages() {
    const headers = {
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    return axios.get(this.apiBaseURL + "pallet_detection/users/data", {
      headers,
    });
  }

  getUserImagesByUserID(id) {
    const headers = {
      Authorization: `Bearer ${this.getAccessToken()}`,
    };
    let url;
    if (id !== null) {
      url =
        this.apiBaseURL +
        `users/get_img_by_id?user_id=${id}&page=1&per_page=10`;
    } else {
      url = this.apiBaseURL + `users/get_img_by_id?page=1&per_page=10`;
    }
    return axios.get(url, { headers });
  }

  getUserPreviousData() {
    const headers = {
      Authorization: `Bearer ${this.getAccessToken()}`,
    };

    return axios.get(this.apiBaseURL + "pallet_detection/user/data", {
      headers,
    });
  }
}
