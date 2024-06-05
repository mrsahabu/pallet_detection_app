import React, { useEffect, useState } from "react";
import ApiService from "../shared/data-service";
import { toast } from "react-toastify";
import UserImagesModal from "../shared/modals/userImages";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";
import ImageDetailsModal from "../shared/modals/imageDetails";
import ProfileModal from "../shared/modals/userProfile";

const AdminDashboard = () => {
  const api = new ApiService();
  const [userVideos, setUsersVideos] = useState([]);
  const [openModal, setOpenModal] = useState(false);
  const [userImages, setUserImages] = useState();
  const [openImageDetailModal, setOpenImageDetailModal] = useState(false);
  const [viewUser, setViewUser] = useState(false);
  const [imageDetails, setImageDetails] = useState();
  const [userDetails, setUserDetails] = useState();

  useEffect(() => {
    toast.loading("Please wait");
    api
      .getALLUsersImages()
      .then((res) => {
        if (res.data) {
          setUsersVideos(res.data);
          toast.dismiss();
        }
      })
      .catch((err) => {
        toast.dismiss();
        toast.error(`Something went wrong ${err}`);
      });
    // eslint-disable-next-line
  }, []);

  const onCloseModal = () => {
    setOpenImageDetailModal(false);
    setViewUser(false);
  };

  const viewUserProfile = (data) => {
    setUserDetails(data.user);
    setViewUser(true);
  };

  const IDCellRenderer = (data) => {
    return (
      <p className="capitalize" style={{ fontSize: "14px" }}>
        {data.buy_or_sell}
      </p>
    );
  };
  
  const dateCellRenderer = (data) => {
    return (
      <p className="capitalize" style={{ fontSize: "14px" }}>
        {data.insert_time.split("T").join(" ")}
      </p>
    );
  };

  const userNameCellRenderer = (data) => {
    return (
      <p
        className="capitalize cursor-pointer hover:underline"
        style={{ fontSize: "14px" }}
        onClick={() => viewUserProfile(data)}
      >
        {data.user.name}
      </p>
    );
  };

  const openConfirmation = (data) => {
    const images = data?.files;
    setUserImages(images);
    setOpenModal(true);
  };

  const openDetailsModal = (data) => {
    setImageDetails(data);
    setOpenImageDetailModal(true);
  };

  const ActionCellRenderer = (data) => {
    return (
      <div className="flex justify-center items-center ">
        <span
          className="pi pi-info-circle cursor-pointer"
          style={{ marginRight: ".5em" }}
          onClick={() => openDetailsModal(data)}
        ></span>
        <span
          className="pi pi-eye cursor-pointer"
          style={{ marginRight: ".5em" }}
          onClick={() => openConfirmation(data)}
        ></span>
      </div>
    );
  };

  return (
    <div className="container mx-auto px-4 py-16">
      <h4 className="mb-3 font-bold text-2xl">Dashboard</h4>

      <div className="card">
        <DataTable value={userVideos} tableStyle={{ minWidth: "50rem" }}>
          <Column field="data_id" header="ID" sortable></Column>
          <Column
            field="user.name"
            header="User Name"
            body={userNameCellRenderer}
            sortable
          ></Column>
          <Column
            field="buy_or_sell"
            header="Buy / Sell"
            body={IDCellRenderer}
            sortable
          ></Column>
          <Column
            field="insert_time"
            header="Date"
            sortable
            body={dateCellRenderer}
          ></Column>
          <Column
            field="pallets_count"
            header="Pallets Count"
            sortable
          ></Column>
          <Column
            header="Action"
            field="pallets_count"
            body={ActionCellRenderer}
            style={{ textAlign: "right" }}
          ></Column>
        </DataTable>
      </div>
      <UserImagesModal
        openModal={openModal}
        setOpenModal={setOpenModal}
        images={userImages}
      />

      <ImageDetailsModal
        isOpen={openImageDetailModal}
        onCloseModal={onCloseModal}
        data={imageDetails}
      />

      <ProfileModal
        isOpen={viewUser}
        onClose={onCloseModal}
        user={userDetails}
      />
    </div>
  );
};

export default AdminDashboard;
