// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Chain {
    struct Post {
        string identifier;
        string creatorId;
        string content;
        bool active;
        uint256 creationTime;
        uint256 updateTime;
    }
    event PostCreated(string indexed postId);

    string[] keys;
    mapping (string => Post[]) public postHistory;

    function createPost(string memory _id, string memory _creatorId, string memory _content) public {
        Post memory newPost = Post({
            identifier: _id,
            creatorId: _creatorId,
            content: _content,
            active: true,
            creationTime: block.timestamp,
            updateTime: block.timestamp
        });

        postHistory[_id].push(newPost);
        keys.push(_id);
        emit PostCreated(_id);
    }

    function getPost(string memory _id) public view returns (Post[] memory) {
        return postHistory[_id];
    }

    function getPosts() external view returns (Post[] memory) {
        Post[] memory posts = new Post[](keys.length);

        for (uint i = 0; i < keys.length; i++) {
            string memory key = keys[i];
            Post[] memory postArray = postHistory[key];

            posts[i] = postArray[postArray.length - 1];
        }

        return posts;
    }

    function setPostContent(string memory _id, string memory _content) public {
        require(bytes(_content).length > 0, "Content cannot be empty");

        Post memory latest = postHistory[_id][postHistory[_id].length - 1];

        latest.content = _content;
        latest.updateTime = block.timestamp;

        postHistory[_id].push(latest);
    }
}
