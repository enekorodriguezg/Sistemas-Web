package servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import HTTPeXist.HTTPeXist;

public class NewImageFile extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // 1. Capturar los datos. "imagenSVG" viene del input oculto que rellenó Javascript
        String svgName = request.getParameter("svgName");
        String collection = request.getParameter("collection");
        String svgContent = request.getParameter("imagenSVG");

        // 2. Validación crítica
        if (svgContent == null || svgContent.trim().isEmpty()) {
            request.setAttribute("informacion", "Error: Archivo vacío. ¿Olvidaste pulsar 'Leer Archivo' antes de enviar?");
            request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
            return;
        }

        if (svgName == null || collection == null || svgName.trim().isEmpty() || collection.trim().isEmpty()) {
            request.setAttribute("informacion", "Error: El nombre del archivo y la colección son obligatorios.");
            request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
            return;
        }

        try {
            // 3. Ejecutar la subida utilizando el orden de parámetros que corregimos (Colección, Contenido, Nombre)
            HTTPeXist api = new HTTPeXist("http://localhost:8080");
            int status = api.subirString(collection, svgContent, svgName);

            if (status >= 200 && status < 300) {
                request.setAttribute("informacion", "Archivo '" + svgName + "' subido con éxito a la colección '" + collection + "'.");
            } else {
                request.setAttribute("informacion", "eXist devolvió un estado de error: " + status);
            }

        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("informacion", "Excepción al subir el archivo: " + e.getMessage());
        }

        // 4. Retorno a la interfaz
        request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }
}