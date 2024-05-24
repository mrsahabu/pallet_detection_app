import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";
import React, { useEffect, useMemo, useState } from "react";
import ApiService from "../shared/data-service";
import { toast } from "react-toastify";

const AdminDashboard = () => {
  const api = new ApiService();
  const [userVideos, setUsersVideos] = useState([]);

  useEffect(() => {
    toast.loading("Please wait");
    api
      .getALLVideos()
      .then((res) => {
        if (res.data) {
          setUsersVideos(res.data);
          toast.dismiss();
        }
      })
      .catch((err) => {
        toast.error(`Something went wrong ${err}`);
      });
    // eslint-disable-next-line
  }, []);

  const IDCellRenderer = ({ data }) => {
    return (
      <div className="action-icons" style={{ cursor: "pointer" }}>
        <p style={{ fontSize: "14px" }}>{data.user_id}</p>
      </div>
    );
  };

  const columnDefs = [
    {
      headerName: "ID",
      field: "id",
      pinned: "left",
      cellRenderer: IDCellRenderer,
    },
    { headerName: " Pallets Count", field: "pallets_count" },
    { headerName: "Image", field: "img_path" },
    { headerName: "Insert Time", field: "insert_time" },
    // {
    //   headerName: "Action",
    //   field: "",
    //   pinned: "right",
    //   cellRenderer: ActionCellRenderer,
    //   filter: false,
    // },
  ];

  const defaultColDef = useMemo(() => {
    return {
      filter: "agTextColumnFilter",
      floatingFilter: true,
    };
  }, []);

  return (
    <div className="container mx-auto px-4 py-32">
      <div className="ag-theme-quartz" style={{ height: "60vh" }}>
        <AgGridReact
          rowData={userVideos}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          pagination={true}
          paginationPageSize={50}
          paginationPageSizeSelector={[50, 100, 200, 500, 1000]}
        />
      </div>
    </div>
  );
};

export default AdminDashboard;
