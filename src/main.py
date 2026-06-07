        """FastAPI entry point for bank-customer-support (Self-Hosted on Azure Container Apps)."""

        import os
        from contextlib import asynccontextmanager
        from dotenv import load_dotenv
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel

        load_dotenv()

        from .agent_runtime import run_agent

# Business Rules:
# Always greet the customer by name. Escalate if unresolved after 3 attempts. Never share internal ticket IDs with customers.

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            print("Starting bank-customer-support...")
            yield
            print("Shutting down bank-customer-support...")


        app = FastAPI(
            title="bank-customer-support",
            description="A customer support agent that can search a knowledge base, create support tickets, track ticket status, and escalate complex issues to human agents when needed. It responds politely, provides step-by-",
            version="1.0.0",
            lifespan=lifespan,
        )


        class InvokeRequest(BaseModel):
            message: str
            session_id: str | None = None


        class InvokeResponse(BaseModel):
            response: str
            session_id: str | None = None


        @app.get("/health")
        async def health():
            return {"status": "healthy", "agent": "bank-customer-support"}


        @app.post("/invoke", response_model=InvokeResponse)
        async def invoke(req: InvokeRequest):
            """Invoke the agent with a message."""
            try:
                result = await run_agent(req.message)
                return InvokeResponse(response=result, session_id=req.session_id)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
