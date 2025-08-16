"""
API Routes for Banking RAG System

Flask Blueprint containing all API endpoints for the Banking RAG system.
"""

from datetime import datetime
import time
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file
from core.rag_service import BankingRAGService
from models import BankingDocument
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import json
import os

# Create blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

@api_blueprint.route('/', methods=['GET'])
def home():
    """Render the home page."""
    try:
        if not rag_service.is_initialized:
            rag_service.initialize()
        
        # Get system statistics
        stats = {
            "total_documents": len(rag_service.documents),
            "categories": set(doc.category for doc in rag_service.documents),
            "response_time": 150  # placeholder average response time in ms
        }
        
        return render_template('home.html', 
                             active_page='home',
                             stats=stats)
        
    except Exception as e:
        flash(f'Error loading statistics: {str(e)}', 'error')
        return render_template('home.html', 
                             active_page='home',
                             stats={"total_documents": 0, "categories": [], "response_time": 0})

@api_blueprint.route('/add-qsa', methods=['GET', 'POST'])
def add_qsa():
    """Handle adding new Q&A documents through web interface."""
    if request.method == 'POST':
        try:
            # Get form data
            question = request.form.get('question')
            answer = request.form.get('answer')
            category = request.form.get('category')
            source = request.form.get('source', 'Web Interface')
            
            if not all([question, answer, category]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('api.add_qsa'))

            # Create new document
            new_doc = BankingDocument(
                id=f'doc_{int(time.time())}',
                title=question[:50] + '...',
                content=f'Q: {question}\nA: {answer}',
                category=category,
                source=source,
                date_added=datetime.now().isoformat()
            )

            # Add to knowledge base
            rag_service.add_document(new_doc)
            
            # Trigger reindex
            rag_service.reindex()

            flash('Document added successfully!', 'success')
            return redirect(url_for('api.add_qsa'))

        except Exception as e:
            flash(f'Error adding document: {str(e)}', 'error')
            return redirect(url_for('api.add_qsa'))

    # GET request - show form
    categories = [
        'Personal Loans',
        'Savings & Checking',
        'Credit Cards',
        'Investments',
        'Mobile Banking',
        'Mortgages',
        'Business Banking',
        'Regulations',
        'Customer Support',
        'Digital Assets',
        'Wealth Management'
    ]
    
    return render_template('add_qsa.html', 
                         active_page='add_qsa',
                         categories=categories)

# Global RAG service instance (will be set by the main app)
rag_service: BankingRAGService = None

def set_rag_service(service: BankingRAGService):
    """Set the RAG service instance for the API routes."""
    global rag_service
    rag_service = service

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    """Check service health status."""
    try:
        status = rag_service.get_health_status()
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "service_info": status
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/query', methods=['POST'])
def process_query():
    """Process a banking question and return AI-generated response."""
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'query' field in request body"
            }), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({
                "status": "error", 
                "message": "Query cannot be empty"
            }), 400
        
        # Process the query
        result = rag_service.answer_question(query)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/categories', methods=['GET'])
def get_categories():
    """Get available document categories."""
    try:
        if not rag_service.is_initialized:
            rag_service.initialize()
        
        categories = {}
        for doc in rag_service.documents:
            if doc.category not in categories:
                categories[doc.category] = []
            categories[doc.category].append({
                "id": doc.id,
                "title": doc.title,
                "source": doc.source
            })
        
        return jsonify({
            "status": "success",
            "categories": categories,
            "total_documents": len(rag_service.documents),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/batch', methods=['POST'])
def process_batch_queries():
    """Process multiple queries in batch."""
    try:
        data = request.get_json()
        
        if not data or 'queries' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'queries' field in request body"
            }), 400
        
        queries = data['queries']
        
        if not isinstance(queries, list) or len(queries) == 0:
            return jsonify({
                "status": "error",
                "message": "Queries must be a non-empty list"
            }), 400
        
        if len(queries) > 10:  # Limit batch size
            return jsonify({
                "status": "error", 
                "message": "Maximum 10 queries per batch"
            }), 400
        
        # Process all queries
        results = []
        for i, query in enumerate(queries):
            if isinstance(query, str) and query.strip():
                result = rag_service.answer_question(query.strip())
                result['batch_index'] = i
                results.append(result)
            else:
                results.append({
                    "batch_index": i,
                    "status": "error",
                    "message": "Invalid query format"
                })
        
        return jsonify({
            "status": "success",
            "results": results,
            "batch_size": len(queries),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/documents', methods=['GET', 'POST'])
def manage_documents():
    """Manage documents in the knowledge base."""
    if request.method == 'GET':
        try:
            documents = rag_service.list_documents()
            
            return jsonify({
                "status": "success",
                "documents": documents,
                "total_documents": len(documents),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500
    
    elif request.method == 'POST':
        """Add a new document to the knowledge base."""
        try:
            data = request.get_json()
            
            required_fields = ['id', 'title', 'content', 'category', 'source']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }), 400
            
            # Create new document
            new_doc = BankingDocument(
                id=data['id'],
                title=data['title'],
                content=data['content'],
                category=data['category'],
                source=data['source']
            )
            
            # Add to RAG service
            success = rag_service.add_document(new_doc)
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": "Document added successfully",
                    "document_id": new_doc.id,
                    "total_documents": len(rag_service.documents),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to add document",
                    "timestamp": datetime.now().isoformat()
                }), 500
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500

@api_blueprint.route('/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document from the knowledge base."""
    try:
        success = rag_service.remove_document(doc_id)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Document {doc_id} deleted successfully",
                "total_documents": len(rag_service.documents),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Document {doc_id} not found",
                "timestamp": datetime.now().isoformat()
            }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/reindex', methods=['POST'])
def reindex_documents():
    """Rebuild the vector index with current documents."""
    try:
        rag_service.rebuild_index()
        
        return jsonify({
            "status": "success",
            "message": "Vector index rebuilt successfully",
            "total_documents": len(rag_service.documents),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/financial-analysis', methods=['GET'])
def financial_analysis():
    """Render the financial analysis page."""
    return render_template('financial_analysis.html', active_page='financial')

@api_blueprint.route('/risk-analysis', methods=['POST'])
def risk_analysis():
    """Process CSV file and return risk metrics."""
    temp_path = None
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if not file.filename:
            return jsonify({"status": "error", "message": "No file selected"}), 400
            
        # Get parameters
        asset_name = request.form.get('assetName', 'Unknown Asset')
        rf = float(request.form.get('rf', 0.0))
        freq = request.form.get('freq', 'D')
            
        # Get file extension and create temp file
        file_ext = Path(file.filename).suffix.lower()
        suffix = '.xlsx' if file_ext in ['.xlsx', '.xls'] else '.csv'
        
        # Create a temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix=suffix)
        os.close(temp_fd)  # Close the file descriptor immediately
        
        # Save uploaded file to temporary location
        file.save(temp_path)
        
        # Read the file based on its type
        if file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(temp_path)
        else:
            df = pd.read_csv(temp_path)

        try:
            # Convert column names to lowercase for case-insensitive matching
            df.columns = [col.lower() for col in df.columns]
            
            # Find date and close columns
            date_col = next((col for col in df.columns if col.lower() in ['date', 'time', 'timestamp']), None)
            close_col = next((col for col in df.columns if col.lower() in ['close', 'adj close', 'adj_close', 'price']), None)
            
            if not date_col or not close_col:
                return jsonify({
                    "status": "error", 
                    "message": "File must contain Date/Time and Close/Price columns"
                }), 400

            # Rename columns to standard names
            df = df[[date_col, close_col]]
            df.columns = ['Date', 'Close']

            # Convert to numeric and handle errors
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
            if df['Close'].isna().any():
                return jsonify({
                    "status": "error",
                    "message": "Price/Close column contains invalid numeric values"
                }), 400

            # Calculate metrics
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            ret = df['Close'].pct_change().dropna()

            if len(ret) < 2:
                return jsonify({
                    "status": "error",
                    "message": "Not enough valid price data to calculate metrics"
                }), 400

            # Calculate key metrics
            periods = {'D': 252, 'W': 52, 'M': 12}[freq]
            vol_ann = float(ret.std() * np.sqrt(periods))
            sharpe = float((ret.mean() * periods - rf) / (vol_ann if vol_ann != 0 else float('nan')))
            mdd = float((df['Close'] / df['Close'].cummax() - 1.0).min())
            
            # Calculate VaR/CVaR
            var95 = float(np.percentile(ret, 5))
            var99 = float(np.percentile(ret, 1))
            cvar95 = float(ret[ret <= var95].mean())
            cvar99 = float(ret[ret <= var99].mean())
            
            # Calculate CAGR
            n_years = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days / 365.25
            cagr = float((df['Close'].iloc[-1] / df['Close'].iloc[0]) ** (1 / n_years) - 1.0)

            # Prepare results
            metrics = {
                "start": df['Date'].iloc[0].strftime('%Y-%m-%d'),
                "end": df['Date'].iloc[-1].strftime('%Y-%m-%d'),
                "cagr": float(cagr),
                "vol_ann": vol_ann,
                "sharpe": sharpe,
                "max_dd": mdd,
                "var95": var95,
                "var99": var99,
                "cvar95": cvar95,
                "cvar99": cvar99
            }

            # Risk bucket classification
            if vol_ann < 0.10 and abs(mdd) < 0.15:
                bucket = "Conservative"
                alloc = {"Bonds/Deposits": 70, "Equities": 25, "Alternatives/Cash": 5}
            elif vol_ann < 0.18 and abs(mdd) < 0.30:
                bucket = "Moderate"
                alloc = {"Bonds/Deposits": 40, "Equities": 55, "Alternatives/Cash": 5}
            else:
                bucket = "Aggressive"
                alloc = {"Bonds/Deposits": 20, "Equities": 75, "Alternatives/Cash": 5}

            # Build mind map
            mindmap = {
                "id": "asset",
                "label": f"Asset: {asset_name} ({metrics['start']} → {metrics['end']})",
                "children": [
                    {
                        "id": "metrics",
                        "label": "Risk Metrics",
                        "children": [
                            {"id": "cagr", "label": f"CAGR: {metrics['cagr']*100:.2f}%"},
                            {"id": "vol", "label": f"Vol (Ann.): {metrics['vol_ann']*100:.2f}%"},
                            {"id": "sh", "label": f"Sharpe: {metrics['sharpe']:.2f}"},
                            {"id": "mdd", "label": f"Max DD: {metrics['max_dd']*100:.2f}%"},
                            {"id": "var", "label": f"VaR95/99: {metrics['var95']*100:.2f}% / {metrics['var99']*100:.2f}%"},
                            {"id": "cvar", "label": f"CVaR95/99: {metrics['cvar95']*100:.2f}% / {metrics['cvar99']*100:.2f}%"}
                        ]
                    },
                    {
                        "id": "profile",
                        "label": f"Risk Profile: {bucket}",
                        "children": [
                            {"id": "alloc", "label": "Suggested Allocation"},
                            *[{"id": k.lower(), "label": f"{k}: {v}%"} for k, v in alloc.items()]
                        ]
                    }
                ]
            }

            return jsonify({
                "status": "success",
                "metrics": metrics,
                "profile": {"risk_bucket": bucket, "alloc": alloc},
                "mindmap": mindmap
            })

        except Exception as e:
            # Log the detailed error for debugging
            print(f"Error processing data: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Error processing data. Please check the format of your file."
            }), 400

    except Exception as e:
        # Log the error for debugging
        print(f"Error in risk analysis: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred. Please try again."
        }), 500

    finally:
        # Make sure the temp file is deleted if it still exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"Error deleting temp file: {str(e)}")

# @api_blueprint.route('/ifrs-report', methods=['POST'])
# def _render_ifrs_html(data):
#     """
#     Generate HTML report from IFRS JSON data.
#     Args:
#         data (dict): IFRS report data in JSON format
#     Returns:
#         str: HTML formatted report
#     """
#     try:
#         # Extract key sections from data
#         company_info = data.get('company_info', {})
#         financial_statements = data.get('financial_statements', {})
#         notes = data.get('notes', [])
        
#         # Generate HTML sections
#         html = '<div class="ifrs-report">'
        
#         # Company Info Section
#         html += '<div class="section company-info">'
#         html += f'<h3>{company_info.get("name", "Company")} - IFRS Report</h3>'
#         html += f'<p>Period: {company_info.get("period", "Not specified")}</p>'
#         html += f'<p>Date: {company_info.get("date", "Not specified")}</p>'
#         html += '</div>'
        
#         # Financial Statements Section
#         if financial_statements:
#             html += '<div class="section financial-statements">'
#             html += '<h4>Financial Statements</h4>'
            
#             # Balance Sheet
#             if 'balance_sheet' in financial_statements:
#                 html += _render_statement_table(
#                     'Balance Sheet',
#                     financial_statements['balance_sheet']
#                 )
            
#             # Income Statement
#             if 'income_statement' in financial_statements:
#                 html += _render_statement_table(
#                     'Income Statement',
#                     financial_statements['income_statement']
#                 )
            
#             # Cash Flow Statement
#             if 'cash_flow' in financial_statements:
#                 html += _render_statement_table(
#                     'Cash Flow Statement',
#                     financial_statements['cash_flow']
#                 )
                
#             html += '</div>'
        
#         # Notes Section
#         if notes:
#             html += '<div class="section notes">'
#             html += '<h4>Notes to Financial Statements</h4>'
#             for i, note in enumerate(notes, 1):
#                 html += f'<div class="note"><strong>Note {i}:</strong> {note}</div>'
#             html += '</div>'
        
#         html += '</div>'
#         return html
        
#     except Exception as e:
#         print(f"Error generating IFRS HTML: {str(e)}")
#         raise

# def _render_statement_table(title, data):
#     """
#     Helper function to render financial statement tables.
#     Args:
#         title (str): Table title
#         data (dict): Statement data
#     Returns:
#         str: HTML table
#     """
#     html = f'<div class="statement"><h5>{title}</h5><table class="table table-bordered">'
    
#     # Headers
#     html += '<thead><tr>'
#     html += '<th>Item</th>'
#     if isinstance(data, dict) and 'periods' in data:
#         for period in data['periods']:
#             html += f'<th>{period}</th>'
#     html += '</tr></thead>'
    
#     # Body
#     html += '<tbody>'
#     if isinstance(data, dict):
#         for item, values in data.get('items', {}).items():
#             html += '<tr>'
#             html += f'<td>{item}</td>'
#             if isinstance(values, list):
#                 for value in values:
#                     html += f'<td class="text-end">{_format_number(value)}</td>'
#             html += '</tr>'
#     html += '</tbody></table></div>'
    
#     return html

# def _format_number(value):
#     """
#     Format numbers for display in IFRS report.
#     Args:
#         value: Number to format
#     Returns:
#         str: Formatted number string
#     """
#     try:
#         if isinstance(value, (int, float)):
#             if abs(value) >= 1_000_000:
#                 return f"{value/1_000_000:.2f}M"
#             elif abs(value) >= 1_000:
#                 return f"{value/1_000:.1f}K"
#             else:
#                 return f"{value:.2f}"
#         return str(value)
#     except:
#         return str(value)

def ifrs_report():
    """Generate IFRS report from JSON data."""
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if not file.filename:
            return jsonify({"status": "error", "message": "No file selected"}), 400

        # Read and validate JSON
        try:
                        data = json.loads(file.read())
        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON file"}), 400

        #     file_content = file.read().decode('utf-8')  # Decode bytes to string
        #     data = json.loads(file_content)
        # except UnicodeDecodeError:
        #     return jsonify({"status": "error", "message": "File must be UTF-8 encoded"}), 400
        # except json.JSONDecodeError as e:
        #     return jsonify({
        #         "status": "error", 
        #         "message": f"Invalid JSON file: {str(e)}. Please ensure the file contains valid JSON data."
        #     }), 400

        # Generate HTML report
        html = _render_ifrs_html(data)
        
        # Return HTML content as JSON response
        return jsonify({
            "status": "success",
            "html": html,
            "message": "Report generated successfully"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
