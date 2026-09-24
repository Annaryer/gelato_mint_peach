
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import get_connection, create_table


app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_table()

app.mount("/Static", StaticFiles(directory="Static"), name="Static")
templates = Jinja2Templates(directory="Templates")
@app.get("/")
def home(request: Request):
    conn = get_connection()
    icecreams = conn.execute(
        "SELECT * FROM icecream"
    ).fetchall()
    conn.close()

    return templates.TemplateResponse(
        request,
        "index.html",
        {"icecreams": icecreams}
    )


@app.get("/menu")
def menu(request: Request):
    conn = get_connection()
    icecreams = conn.execute(
        "SELECT * FROM icecream"
    ).fetchall()
    conn.close()

    return templates.TemplateResponse(
        request,
        "menu.html",
        {"icecreams": icecreams}
    )

@app.get("/order")
def order(request: Request):
    conn = get_connection()

    icecreams = conn.execute(
        "SELECT * FROM icecream"
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request,
        "order.html",
        {
            "icecreams": icecreams
        }
    )


@app.post("/order")
def create_order(
        request: Request,
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone: str = Form(...),
        selected_items: str = Form(...),
        total_price: int = Form(...),
        message: str = Form("")
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO orders
        (first_name, last_name, phone, items, total_price)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            first_name,
            last_name,
            phone,
            selected_items,
            total_price
        )
    )

    conn.commit()

    icecreams = conn.execute(
        "SELECT * FROM icecream"
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request,
        "order.html",
        {
            "icecreams": icecreams,
            "order_success": True,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        }
    )


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        request,
        "about.html"
    )

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(
        request,
        "contact.html",
        {"message_sent": False}
    )


@app.post("/contact")
def send_message(
        request: Request,
        name: str = Form(...),
        email: str = Form(...),
        message: str = Form(...)
):
    return templates.TemplateResponse(
        request,
        "contact.html",
        {
            "message_sent": True,
            "name": name
        }
    )

@app.post("/add")
def add_icecream(
        name: str = Form(...),
        type: str = Form(...),
        price: int = Form(...)
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO icecream (name, type, price)
        VALUES (?, ?, ?)
        """,
        (name, type, price)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.get("/delete/{id}")
def delete_icecream(id: int):
    conn = get_connection()

    conn.execute(
        "DELETE FROM icecream WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        "/",
        status_code=303
    )

@app.get("/edit/{id}")
def edit_icecream(id: int, request: Request):
    conn = get_connection()

    icecream = conn.execute(
        "SELECT * FROM icecream WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if icecream is None:
        return RedirectResponse(
            "/",
            status_code=303
        )

    return templates.TemplateResponse(
        request,
        "edit.html",
        {"icecream": icecream}
    )


@app.post("/update/{id}")
def update_icecream(
        id: int,
        name: str = Form(...),
        type: str = Form(...),
        price: int = Form(...)
):
    conn = get_connection()

    conn.execute(
        """
        UPDATE icecream
        SET name=?, type=?, price=?
        WHERE id=?
        """,
        (name, type, price, id)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        "/",
        status_code=303
    )

