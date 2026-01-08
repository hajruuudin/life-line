import React, { useEffect, useRef } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { authService } from "../services/auth";

function GoogleCallbackPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const hasProcessed = useRef(false); // Prevent duplicate processing

  useEffect(() => {
    const handleCallback = async () => {
      // Prevent duplicate requests (React.StrictMode runs effects twice in development)
      if (hasProcessed.current) {
        return;
      }
      hasProcessed.current = true;

      try {
        const code = searchParams.get("code");
        const error = searchParams.get("error");

        if (error) {
          navigate("/login?error=" + error);
          return;
        }

        if (!code) {
          navigate("/login?error=No+code+received");
          return;
        }

        // Call backend to exchange code for token
        const result = await authService.handleCallback(code);
        // Token is already stored in localStorage by handleCallback()
        // Add a small delay before redirect to ensure localStorage is persisted
        setTimeout(() => {
          window.location.replace("/");
        }, 100);
      } catch (error) {
        navigate("/login?error=" + encodeURIComponent(error.message));
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        color: "var(--text-primary)",
      }}
    >
      <p>Completing authentication...</p>
    </div>
  );
}

export default GoogleCallbackPage;
