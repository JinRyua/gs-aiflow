import React from "react";
import { useQuery } from "react-query";
import axios from "axios";
import { useState} from 'react';
import { Space, Table, Tag, Button, Modal } from 'antd';
import { useNavigate } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import CreateProjectModal from './create_project_modal';
const getProjectList = async ( id ) => {
    const { data } = await axios.get(process.env.REACT_APP_API+'/api/getProjectList/' + id);
    var list = data.project_list;
    var count = 0;
    list.forEach(function(item){
        item.key = count;
        count++;
    })
    console.log(list)
    return list;
    
  };

  const columns = [
    {
      title: '프로젝트 이름',
      dataIndex: 'project_name',
      key: 'project_name',
      width:400,
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <a>Delete</a>
        </Space>
      ),
    },
  ];

function ProjectList(props) {
    var id = props.id;
    const setPage = props.setPage;
    const [nameValidation, setNameValidation] = useState(false);
    const [projectName, setProjectName] = useState("");
    const [projectDesc, setProjectDesc] = useState("");
    const [clusterList, setClusterList] = useState([]);


    const navigate = useNavigate();
    const { isLoading, isError, data, error } = useQuery(["projectList"], () => {return getProjectList(id)}, {
        refetchOnWindowFocus:false,
        retry:0,
    });

    const initCreateProjectData = () =>{
      setNameValidation(false);
      setProjectName("");
      setProjectDesc("");
      setClusterList([]);
    }
    
    const onRow = (record, rowIndex) => {
        return {
          onClick: (event) => {
              // record: row의 data
              // rowIndex: row의 index
              // event: event prototype
            console.log(record, rowIndex, event);
            navigate('/monitoring/' + record.project_name)
            setPage('monitoring')
          },
        };
      };

    const createProject = () => {
      initCreateProjectData();
      showModal();
    }

    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [modalText, setModalText] = useState('Content of the modal');
  
    const showModal = () => {
      setOpen(true);
    };


    var specialNameRegex = /^[A-Za-z0-9\-]+$/;
    var specialDescRegex = /^[ㄱ-ㅎ가-힣A-Za-z0-9\s]+$/;

    const validateProjectName = (name) => {
      if(name == ''){
        return false;
      }
      else{
        return specialNameRegex.test(name);
      }
    }

    const validateProjectDesc = (desc) => {
      return specialDescRegex.test(desc);
    }

    const validateClusterList = (desc) => {
      if(desc.length == 0){
        return false;
      }
      return true;
    }
  
    const handleOk = () => {
      if(!nameValidation){
        console.log("val")
      }
      else if(!validateProjectName(projectName)){
        console.log("name")
      }
      else if(!validateProjectDesc(projectDesc)){
        console.log("desc")
      }
      else if(!validateClusterList(clusterList)){
        console.log("cluster")
      }
      else{
        setModalText('The modal will be closed after two seconds');
        setConfirmLoading(true);
        setTimeout(() => {
          setOpen(false);
          setConfirmLoading(false);
        }, 2000);
      }
      
    };
  
    const handleCancel = () => {
      console.log('Clicked cancel button');
      setOpen(false);
    };

    return (
        <> < div id = 'service_define_main' > 
        <div style={{display:'flex'}} >
          <h2>목록</h2>
        <div align='right' style={{flex:1, display:'flex', justifyContent:'flex-end'}}> 
          {/* <h2 >프로젝트 목록</h2>  */}
          <Button style={{margin:'auto 0'}} type="primary" icon={<PlusOutlined />} onClick={createProject}>
            New Project
          </Button>
        </div>
        </div>

    {
        !isLoading && (
            <Table rowKey={"project_name"} columns={columns} dataSource={data} onRow={onRow} pagination={{ pageSize: 5, showSizeChanger:false}}/>
            // <h1>{data}</h1>
        )

    }
    
    <Modal
        title="프로젝트 생성"
        open={open}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        destroyOnClose={true}
      >
        <div style={{height:'10px'}}/>
        <CreateProjectModal id={id} validation={{
          nameValidation:[nameValidation, setNameValidation],
          projectName:[projectName, setProjectName],
          projectDesc:[projectDesc, setProjectDesc],
          clusterList:[clusterList, setClusterList]
          }} />
      </Modal>
    </div>
    </>
    
    );
}

export {
    ProjectList
};
