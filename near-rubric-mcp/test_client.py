#!/usr/bin/env python
"""
Test client for NEAR Rubric MCP Server.
This script demonstrates how to call the MCP server tools.
"""

import json
import sys
import subprocess
import os
import tempfile
import glob
from typing import Dict, Any, List

def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call a tool from the MCP server.
    
    Args:
        tool_name: The name of the tool to call
        arguments: The arguments to pass to the tool
        
    Returns:
        Dict containing the tool response
    """
    request = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }
    
    # Create a temporary file for the request
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp:
        temp_path = temp.name
        json.dump(request, temp)
    
    try:
        # Launch server process with the input file
        cmd = f'python server.py < {temp_path}'
        if os.name == 'nt':  # Windows
            cmd = f'type {temp_path} | python server.py'
        
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            check=False
        )
        
        # Parse the response
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response",
                "raw": result.stdout,
                "stderr": result.stderr
            }
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_path)
        except:
            pass

def print_json(data: Dict[str, Any], indent: int = 2) -> None:
    """Print JSON data in a pretty format."""
    if isinstance(data, dict) and "result" in data:
        # For JSON-RPC responses, just print the result part
        print(json.dumps(data["result"], indent=indent))
    else:
        print(json.dumps(data, indent=indent))

def test_get_evaluation_framework():
    """Test the get_evaluation_framework tool."""
    print("Testing get_evaluation_framework...")
    response = call_tool("get_evaluation_framework", {
        "category": "near_integration",
        "project_type": "rust"
    })
    print_json(response)

def test_get_file_suggestions():
    """Test the get_file_suggestions tool."""
    print("\nTesting get_file_suggestions...")
    
    # More varied file path examples to demonstrate improved pattern matching
    mock_files = [
        "src/contract.rs",
        "src/lib.rs",
        "Cargo.toml",
        "src/utils.rs",
        "README.md",
        "frontend/near-wallet.js",
        "contracts/main_contract.rs",
        "contracts/src/lib.rs",
        "web/src/components/NearLogin.jsx",
        "web/src/components/NearWallet.tsx",
        "scripts/deploy.js",
        "tests/contract.test.js",
        "docs/NEAR_INTEGRATION.md",
        "package.json",
        "node_modules/near-api-js/lib/index.js"
    ]
    
    # Test pattern matching for different categories
    categories_to_test = [
        "near_integration",  # Test standard category
        "1. NEAR Protocol Integration",  # Test with number prefix
        "onchain_quality",  # Test another category
        "code_quality"  # Test a category with different file patterns
    ]
    
    for category in categories_to_test:
        print(f"\nTesting file suggestions for category: {category}")
        response = call_tool("get_file_suggestions", {
            "category": category,
            "available_files": mock_files
        })
        print_json(response)

def test_analyze_code_context():
    """Test the analyze_code_context tool."""
    print("\nTesting analyze_code_context...")
    
    # Sample code context (would normally be extracted by client)
    code_context = {
        "src/lib.rs": """use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::{env, near_bindgen, AccountId, Balance, Promise};

#[near_bindgen]
#[derive(Default, BorshDeserialize, BorshSerialize)]
pub struct Contract {
    owner_id: AccountId,
    total_supply: Balance,
}

#[near_bindgen]
impl Contract {
    #[init]
    pub fn new(owner_id: AccountId) -> Self {
        Self {
            owner_id,
            total_supply: 0,
        }
    }
    
    pub fn get_owner(&self) -> AccountId {
        self.owner_id.clone()
    }
    
    #[payable]
    pub fn transfer(&mut self, to: AccountId) {
        let amount = env::attached_deposit();
        let sender = env::predecessor_account_id();
        
        // Transfer logic here
        Promise::new(to).transfer(amount);
        
        env::log_str(&format!("Transferred {} from {} to {}", amount, sender, to));
    }
}""",
        "frontend/near-wallet.js": """import { connect, WalletConnection, keyStores } from 'near-api-js';

export class NearWallet {
  constructor() {
    this.config = {
      networkId: 'testnet',
      keyStore: new keyStores.BrowserLocalStorageKeyStore(),
      nodeUrl: 'https://rpc.testnet.near.org',
      walletUrl: 'https://wallet.testnet.near.org',
      helperUrl: 'https://helper.testnet.near.org',
      explorerUrl: 'https://explorer.testnet.near.org',
    };
  }

  async connect() {
    // Connect to NEAR
    const near = await connect(this.config);
    
    // Create wallet connection
    this.walletConnection = new WalletConnection(near);
    
    // Get account
    this.account = this.walletConnection.account();
    
    return this.walletConnection.isSignedIn();
  }
  
  signIn() {
    // Redirect to wallet for signing in
    this.walletConnection.requestSignIn({
      contractId: 'mycontract.testnet',
      successUrl: window.location.href,
      failureUrl: window.location.href,
    });
  }
  
  signOut() {
    this.walletConnection.signOut();
    window.location.reload();
  }
  
  async callMethod(method, args = {}) {
    // Call a contract method
    return await this.account.functionCall({
      contractId: 'mycontract.testnet',
      methodName: method,
      args: args,
      attachedDeposit: 0,
    });
  }
}"""
    }
    
    response = call_tool("analyze_code_context", {
        "category": "near_integration",
        "code_context": code_context
    })
    print_json(response)

def test_pattern_matching_with_complex_extensions():
    """Test pattern matching with complex file extensions."""
    print("\nTesting pattern matching with complex file extensions...")
    
    # Files with various extensions to test patterns like "*.{js,ts,jsx,tsx}"
    mock_files = [
        "src/components/Button.js",
        "src/components/Wallet.jsx",
        "src/utils/near.ts",
        "src/pages/Dashboard.tsx",
        "contract/Counter.rs",
        "contract/src/lib.rs",
        "contract/tests/integration.rs",
        "src/styles/main.css",
        "src/assets/logo.png",
        "package.json",
        "webpack.config.js"
    ]
    
    # The offchain_quality category has patterns with {js,ts,jsx,tsx} extensions
    response = call_tool("get_file_suggestions", {
        "category": "offchain_quality",
        "available_files": mock_files
    })
    print_json(response)

def test_analyze_pattern_matches():
    """Test the analyze_pattern_matches tool."""
    print("\nTesting analyze_pattern_matches...")
    
    # Sample code content for pattern analysis (simplified for testing)
    code_content = {
        "src/contract.rs": """use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::{env, near_bindgen, AccountId, Balance};

#[near_bindgen]
pub struct Contract {
    owner_id: AccountId,
}

#[near_bindgen]
impl Contract {
    pub fn get_owner(&self) -> AccountId {
        self.owner_id.clone()
    }
}""",
        "src/app.js": """import { connect, WalletConnection } from 'near-api-js';

function signIn(wallet) {
    wallet.requestSignIn({
        contractId: 'mycontract.testnet'
    });
}"""
    }
    
    # Test pattern matching for near_integration category
    category = "near_integration"
    print(f"\nAnalyzing pattern matches for category: {category}")
    response = call_tool("analyze_pattern_matches", {
        "category": category,
        "code_content": code_content,
        "project_type": "mixed"
    })
    print_json(response)

def test_monorepo():
    """Test with actual monorepo files."""
    print("\nTesting with actual monorepo files...")
    
    # Get all the files in the monorepo
    monorepo_path = "../repos_to_audit/monorepo"
    all_files = []
    
    # Track file extensions for summary
    extension_counts = {}
    
    # Find all files in the monorepo recursively
    for root, dirs, files in os.walk(monorepo_path):
        for file in files:
            # Convert absolute path to relative path from monorepo root
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, start=monorepo_path)
            all_files.append(relative_path)
            
            # Count file extensions
            ext = os.path.splitext(file)[1].lower()
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
    
    # Print summary of file extensions
    print("\nFile extension summary:")
    for ext, count in sorted(extension_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 5:  # Only show extensions with more than 5 files
            print(f"{ext}: {count} files")
    
    # Collect specific file types for NEAR analysis
    near_relevant_files = []
    
    # Look for Rust, JavaScript, TypeScript files and common config files
    for file in all_files:
        if (file.endswith('.rs') or 
            file.endswith('.js') or 
            file.endswith('.ts') or 
            file.endswith('.tsx') or 
            file.endswith('.jsx') or
            'contract' in file.lower() or
            'near' in file.lower() or
            file.endswith('Cargo.toml') or
            file.endswith('package.json')):
            near_relevant_files.append(file)
    
    # Limit to a reasonable number for testing
    sample_files = near_relevant_files[:200]  # Limit to first 200 relevant files
    print(f"\nFound {len(sample_files)} potentially relevant files out of {len(all_files)} total files")
    
    # Test file suggestions for NEAR integration
    print(f"\nTesting file suggestions for monorepo...")
    response = call_tool("get_file_suggestions", {
        "category": "near_integration",
        "available_files": sample_files
    })
    print_json(response)
    
    # Extract suggested files from response
    suggested_files = response.get("result", {}).get("suggested_files", [])
    
    if suggested_files:
        print(f"\nFound {len(suggested_files)} suggested files for analysis")
        
        # Read content of the first suggested file for demonstration
        if len(suggested_files) > 0:
            file_to_analyze = suggested_files[0]
            full_path = os.path.join(monorepo_path, file_to_analyze)
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Use analyze_pattern_matches to analyze the file
                print(f"\nAnalyzing file: {file_to_analyze}")
                response = call_tool("analyze_pattern_matches", {
                    "category": "near_integration",
                    "code_content": {file_to_analyze: file_content},
                    "project_type": "mixed"
                })
                print_json(response)
            except Exception as e:
                print(f"Error reading file {full_path}: {str(e)}")
    else:
        print("No suggested files found for analysis")
        
        # Let's try a different approach - analyze a few Rust files directly
        rust_files = [f for f in sample_files if f.endswith('.rs')]
        if rust_files:
            print(f"\nTrying direct analysis of {min(3, len(rust_files))} Rust files")
            
            for i, file_path in enumerate(rust_files[:3]):  # Analyze up to 3 Rust files
                full_path = os.path.join(monorepo_path, file_path)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    print(f"\nAnalyzing file: {file_path}")
                    response = call_tool("analyze_pattern_matches", {
                        "category": "near_integration",
                        "code_content": {file_path: file_content},
                        "project_type": "rust"
                    })
                    print_json(response)
                except Exception as e:
                    print(f"Error reading file {full_path}: {str(e)}")

if __name__ == "__main__":
    # Uncomment the tests you want to run
    #test_get_evaluation_framework()
    #test_get_file_suggestions()
    #test_analyze_code_context()
    #test_pattern_matching_with_complex_extensions()
    #test_analyze_pattern_matches()
    test_monorepo() 