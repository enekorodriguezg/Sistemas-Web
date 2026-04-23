package servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import HTTPeXist.HTTPeXist;

// ¡SIN ANOTACIÓN @WebServlet! El web.xml de la profesora se encarga del enrutamiento.
public class CreateCollection extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String collection = request.getParameter("collection");

        if (collection == null || collection.trim().isEmpty()) {
            request.setAttribute("informacion", "Error: El nombre de la colección no puede estar vacío.");
            request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
            return;
        }

        try {
            HTTPeXist api = new HTTPeXist("http://localhost:8080");
            api.create(collection);

            request.setAttribute("informacion", "Colección '" + collection + "' creada correctamente.");

        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("informacion", "Error al crear la colección: " + e.getMessage());
        }

        request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }
}