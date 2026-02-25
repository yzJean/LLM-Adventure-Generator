import {useState, useEffect, use} from "react";
import {useParams, useNavigate} from "react-router-dom";
import axios from "axios";
import LoadingStatus from "./LoadingStatus.jsx";
import StoryGame from "./StoryGame.jsx";
import {API_BASE_URL} from "../util.js"

function StoryLoader() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [story, setStory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Execute callback: loadStory(): Fetch the story from backend when this component mounts or when the id parameter changes.
        loadStory(id);
    }, [id]); // The dependency array [id] tells React: "Re-run this effect whenever id changes".

    // function to load story by id
    const loadStory = async(storyId) => {
        setLoading(true);
        setError(null);

        try { // send a request to the backend to get the story data
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
            setStory(response.data);
            // response is the axios wrapper:
            // response = {
            //   status: 200,
            //   data: { ... }, ← CompleteStoryResponse fields
            //   ...
            // }

            // response.data is the actual story:
            // response.data = {
            //   id: 1,
            //   title: "...",
            //   created_at: "...",
            //   root_nodes: {...},
            //   all_nodes: {...}
            // }

            setLoading(false);
        } catch (err) {
            if (err.response?.status == 404) {
                setError("Story not found");
            } else {
                setError("Failed to load story");
            }
        } finally {
            setLoading(false);
        }
    }

    const createNewStory = () => {
        navigate("/")
    }

    if (loading) {
        return <LoadingStatus theme={"story"}/>
    }

    if (error) {
        return <div className="story-loader">
            <div className="error-message">
                <h2>Story Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewStory}>Go to Story Generator</button>
            </div>
        </div>
    }

    if (story) {
        return <div className="story-loader">
            <StoryGame story={story} onNewStory={createNewStory} />
        </div>
    }

}
export default StoryLoader;