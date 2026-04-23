package servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import HTTPeXist.HTTPeXist;

public class DeleteCollection extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // 1. Captura del nombre de la colección desde el formulario
        String collection = request.getParameter("collection");

        // 2. Validación básica
        if (collection == null || collection.trim().isEmpty()) {
            request.setAttribute("informacion", "Error: Debe especificar el nombre de la colección a borrar.");
            request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
            return;
        }

        try {
            // 3. Llamada al método delete(String collection) de tu clase HTTPeXist
            HTTPeXist api = new HTTPeXist("http://localhost:8080");
            int status = api.delete(collection);

            if (status == 200) {
                request.setAttribute("informacion", "Colección '" + collection + "' borrada con éxito.");
            } else if (status == 404) {
                request.setAttribute("informacion", "Error: La colección '" + collection + "' no existe.");
            } else {
                request.setAttribute("informacion", "eXist devolvió un código de estado: " + status);
            }

        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("informacion", "Excepción al borrar la colección: " + e.getMessage());
        }

        // 4. Redirección interna al index para mostrar el mensaje
        request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
    }

    // Permitimos GET por si acaso, redirigiendo a la lógica de POST
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }
}