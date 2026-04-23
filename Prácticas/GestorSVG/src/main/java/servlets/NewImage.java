package servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import HTTPeXist.HTTPeXist;

// ¡SIN ANOTACIÓN @WebServlet! El web.xml se encarga.
public class NewImage extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // 1. CAPTURA DE PARÁMETROS DEL FORMULARIO
        String svgName = request.getParameter("svgName");
        String collection = request.getParameter("collection");

        // 2. VALIDACIÓN ROBUSTA
        if (svgName == null || svgName.trim().isEmpty() ||
                collection == null || collection.trim().isEmpty()) {

            request.setAttribute("informacion", "Error: El nombre de la imagen y la colección destino son obligatorios.");
            request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
            return;
        }

        // 3. CREACIÓN DEL CONTENIDO SVG "EN BLANCO"
        String blankSvg = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
                "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"200\">\n" +
                "  <rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n" +
                "  \n" +
                "</svg>";

        try {
            // 4. LLAMADA A LA CAPA DE DATOS (HTTPeXist)
            HTTPeXist api = new HTTPeXist("http://localhost:8080");
            api.subirString(collection, blankSvg, svgName);

            request.setAttribute("informacion", "Imagen '" + svgName + "' creada correctamente en '" + collection + "'.");

        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("informacion", "Error al crear la imagen: " + e.getMessage());
        }

        // 5. VUELTA AL INDEX CON MENSAJE DE ÉXITO O ERROR
        request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
    }

    // Por seguridad, GET también redirige a POST
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }
}