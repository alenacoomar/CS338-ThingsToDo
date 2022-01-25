import {Card} from "react-bootstrap";

export function ToDoList({ data }) {
    return (
        <div>
            {data ? Object.values(data).map((value) => <Item key={value.name} value={value}/>) : null}
        </div>
    );
}

function Item({ value }) {
    return (
        <Card className="m-2">
            <Card.Body>
                <Card.Title>{value.name}</Card.Title>
                <Card.Text>time: {value.time}</Card.Text>
                <Card.Text>location: {value.location}</Card.Text>
            </Card.Body>
        </Card>

    );
}