import React, { useState } from "react";
import { Typography, Input, Button } from "antd";
import { useDispatch } from "react-redux";
import { getPostsByUser } from "../actions/posts";
import { useSelector } from "react-redux";
import NavArrow from "./NavArrow"

const { Search } = Input;
const aboutStyle = {
  height: "100vh",
  justifyContent: "center",
  alignItem: "center",
  margin: "auto 0",
};
const smaller = {
  paddingLeft: "15vw",
  paddingRight: "15vw",
};
const header = {
  color: "#b7e3fa",
  textAlign: "center",
  paddingTop: "30vh",
  fontSize: "6em",
};
export default function About() {
  const dispatch = useDispatch();
  const [toggle, setToggle] = useState(false)
  const [username, setUsername] = useState("");

  const onSearch = function () {
    const val = username;
    console.log(username);
    let newUser = username.replace("#", "_");
    setToggle(true);
    dispatch(getPostsByUser(newUser));
    setUsername("");
  };

  const posts = useSelector((state) => state.posts);

  return (
    <div style={aboutStyle}>
      <Typography.Title style={header}>
        {" "}
        Welcome to BadGIF <br /> Whats your discord username?{" "}
      </Typography.Title>
      <Search
        enterButton="Search"
        size="large"
        style={smaller}
        placeholder="input search text"
        value={username}
        onSearch={onSearch}
        onChange={(e) => setUsername(e.target.value)}
      />
      {posts.length > 0 ? <NavArrow/>: null}
    </div>
  );
}
