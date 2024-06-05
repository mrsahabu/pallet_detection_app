import React, { useEffect, useState } from "react";
import ApiService from "../shared/data-service";
import { toast } from "react-toastify";
import UserImagesModal from "../shared/modals/userImages";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const UserPreviousRecords = () => {
  const api = new ApiService();
  const [userVideos, setUsersVideos] = useState([]);
  const [openModal, setOpenModal] = useState(false);
  const [userImages, setUserImages] = useState();
  useEffect(() => {
    toast.loading("Please wait");
    api
      .getUserPreviousData()
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

  const IDCellRenderer = (data) => {
    return (
      <div className="action-icons" style={{ cursor: "pointer" }}>
        <p className="capitalize" style={{ fontSize: "14px" }}>
          {data.buy_or_sell}
        </p>
      </div>
    );
  };

  const openConfirmation = (data) => {
    const images = data?.files;
    setUserImages(images);
    setOpenModal(true);
  };

  const dateCellRenderer = (data) => {
    return (
      <p className="capitalize" style={{ fontSize: "14px" }}>
        {data.insert_time.split("T").join(" ")}
      </p>
    );
  };
  
  const ActionCellRenderer = (data) => {
    return (
      <div className="flex justify-center">
        <svg
          className="text-center cursor-pointer"
          onClick={() => openConfirmation(data)}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          width="24"
          height="24"
        >
          <path
            fill="none"
            stroke="#000"
            strokeWidth="2"
            d="M12 4.5c-6 0-10 7.5-10 7.5s4 7.5 10 7.5 10-7.5 10-7.5-4-7.5-10-7.5zm0 10.5c-1.7 0-3-1.3-3-3s1.3-3 3-3 3 1.3 3 3-1.3 3-3 3zm0-4.5c-.8 0-1.5.7-1.5 1.5s.7 1.5 1.5 1.5 1.5-.7 1.5-1.5-.7-1.5-1.5-1.5z"
          />
        </svg>
      </div>
    );
  };

  return (
    <div className="container mx-auto px-4 py-20">
      <h4 className="mb-3 font-bold text-2xl">Uploaded Data</h4>

      <div className="card">
        <DataTable value={userVideos} tableStyle={{ minWidth: "50rem" }}>
        <Column field="data_id" header="ID" sortable></Column>
        <Column
            field="insert_time"
            header="Date"
            sortable
            body={dateCellRenderer}
          ></Column>
          <Column
            field="buy_or_sell"
            header="Buy / Sell"
            body={IDCellRenderer}
            style={{ width: "200px" }} 
            sortable
          ></Column>
          <Column field="co2_fc" header="Co2 FC" sortable></Column>
          <Column
            field="co2_saving_count"
            header="Co2_Saving Count"
            sortable
          ></Column>
          <Column
            field="pallets_count"
            header="pallets Count"
            sortable
          ></Column>
          <Column field="price_piece" header="Price Piece" sortable></Column>
          <Column field="total_price" header="Total Price" sortable></Column>
          <Column
            field="total_transport"
            header="Total Transport"
            sortable
          ></Column>
          <Column
            field="transport_cost"
            header="Transport Cost"
            sortable
          ></Column>
          <Column
            field="transport_fc_count"
            header="Transport FC Count"
            sortable
          ></Column>
          <Column
            header="Action"
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
    </div>
  );
};

export default UserPreviousRecords;
