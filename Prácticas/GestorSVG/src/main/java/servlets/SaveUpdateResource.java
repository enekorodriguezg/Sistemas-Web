package servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import HTTPeXist.HTTPeXist;

public class SaveUpdateResource extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		String collection = request.getParameter("collection");
		String svgName = request.getParameter("svgName");
		String svgContent = request.getParameter("imagenSVG");
		String accion = request.getParameter("actualizar_salva");

		// DEBUG: Mira tu consola de Tomcat al pulsar el botón
		System.out.println("DEBUG -> Coleccion: " + collection);
		System.out.println("DEBUG -> Archivo: " + svgName);
		System.out.println("DEBUG -> Acción: " + accion);

		if (collection == null || svgName == null || svgContent == null) {
			response.sendRedirect(request.getContextPath() + "/jsp/index.jsp");
			return;
		}

		try {
			HTTPeXist api = new HTTPeXist("http://localhost:8080");
			String nombreDestino = svgName;

			// Lógica de ramificación
			if ("save".equals(accion)) {
				nombreDestino = "copia_" + svgName;
			}

			int status = api.subirString(collection, svgContent, nombreDestino);

			if (status >= 200 && status < 300) {
				request.setAttribute("informacion", "Éxito: Imagen guardada como '" + nombreDestino + "'");
			} else {
				request.setAttribute("informacion", "Error de eXist-db: " + status);
			}

		} catch (Exception e) {
			e.printStackTrace();
			request.setAttribute("informacion", "Excepción: " + e.getMessage());
		}

		// REDIRECCIÓN CON CACHE-BUSTER: Forzamos a la lista a refrescarse
		// Al añadir el parámetro 't', engañamos al navegador para que pida la lista de nuevo
		request.getRequestDispatcher("/apiLR?collection=" + collection + "&t=" + System.currentTimeMillis())
				.forward(request, response);
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doPost(request, response);
	}
}