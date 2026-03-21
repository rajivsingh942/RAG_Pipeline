"""
SharePoint Connector (OneDrive, SharePoint Online)
"""
from typing import List, Dict, Any, Optional
from .base import BaseConnector, Document
from .file_processor import FileProcessor


class SharePointConnector(BaseConnector):
    """Connect to Microsoft SharePoint and OneDrive"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client_id = config.get("client_id")
        self.client_secret = config.get("client_secret")
        self.tenant_id = config.get("tenant_id")
        self.site_url = config.get("site_url")  # e.g., https://tenant.sharepoint.com/sites/sitename
        self.folder_path = config.get("folder_path", "/")  # Relative path in SharePoint
        
        self.client = None
        self.file_processor = FileProcessor()
    
    async def connect(self) -> bool:
        """Establish SharePoint connection"""
        try:
            from office365.runtime.auth.client_credential import ClientCredential
            from office365.sharepoint.client_context import ClientContext
            
            credentials = ClientCredential(self.client_id, self.client_secret)
            self.client = ClientContext(self.site_url).with_credentials(credentials)
            
            return await self.validate_connection()
        except Exception as e:
            print(f"SharePoint connection error: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from SharePoint"""
        self.client = None
        return True
    
    async def validate_connection(self) -> bool:
        """Test SharePoint connection"""
        try:
            if not self.client:
                return False
            # Simple test to validate connection
            web = self.client.web
            web.load()
            self.client.execute_query()
            return True
        except Exception:
            return False
    
    async def load_documents(self) -> List[Document]:
        """Load all documents from SharePoint folder"""
        documents = []
        try:
            if not self.client:
                await self.connect()
            
            folder = self.client.web.get_folder_by_server_relative_url(self.folder_path)
            files = folder.files
            files.load()
            self.client.execute_query()
            
            for file in files:
                try:
                    doc = await self._process_sharepoint_file(file)
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    print(f"Error processing SharePoint file: {e}")
        
        except Exception as e:
            print(f"Error loading SharePoint documents: {e}")
        
        return documents
    
    async def search(self, query: str) -> List[Document]:
        """Search documents in SharePoint"""
        try:
            if not self.client:
                await self.connect()
            
            # Use SharePoint search
            result_table = self.client.search.query(f"'{query}'")
            result_table.load()
            self.client.execute_query()
            
            results = []
            for row in result_table.value:
                doc = Document(
                    id=row.get("docid", ""),
                    content=row.get("summary", ""),
                    source=row.get("path", ""),
                    source_type="sharepoint",
                    metadata={
                        "title": row.get("title", ""),
                        "size": int(row.get("size", 0)),
                        "author": row.get("author", ""),
                    }
                )
                results.append(doc)
            
            return results[:10]
        except Exception as e:
            print(f"Error searching SharePoint: {e}")
            return []
    
    async def _process_sharepoint_file(self, file) -> Optional[Document]:
        """Process a SharePoint file"""
        try:
            # Download file to temporary location
            import tempfile
            from pathlib import Path
            
            file_name = file.name
            file_size = file.length
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file_name).suffix) as tmp:
                tmp_path = Path(tmp.name)
                
                # Download file
                with open(tmp_path, "wb") as f:
                    file.download(f).execute_query()
                
                # Process file
                content = await self.file_processor.process(tmp_path)
                
                if content:
                    return Document(
                        id=file.serverRelativeUrl,
                        content=content,
                        source=f"{self.site_url}{file.serverRelativeUrl}",
                        source_type="sharepoint",
                        metadata={
                            "filename": file_name,
                            "size": file_size,
                            "sharepoint_url": f"{self.site_url}{file.serverRelativeUrl}",
                        }
                    )
                
                # Cleanup
                tmp_path.unlink()
        
        except Exception as e:
            print(f"Error processing SharePoint file: {e}")
        
        return None
