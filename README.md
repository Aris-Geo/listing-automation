# eBay Listing Automation

A Python-based automation workflow to streamline the process of preparing product listings for eBay through Seller Cloud.

## 🚀 Project Overview

This automation tool processes the daily eBay unlisted report (Excel file) and performs all necessary transformations to make products ready for listing on eBay, following Focus Camera's established business rules.

The workflow handles:
- Data cleaning and validation
- Certified refurbished item processing
- Quantity adjustments
- Shipping dimension verification
- Platform restriction checking
- Best offer rule application
- Global shipping eligibility determination
- Shipping template assignment

## 📋 Prerequisites

- Python 3.8+
- Pandas (`pip install pandas`)
- Openpyxl (`pip install openpyxl`)

## 📁 Project Structure

```
listing-automation/
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies
├── main.py                   # Main orchestrator
├── data_loader.py            # File loading functions
├── data_cleaner.py           # Data cleaning functions
├── transformers/             # Business logic modules
│   ├── __init__.py
│   ├── certified_refurbished.py
│   ├── quantity_handler.py
│   ├── subtitle_handler.py
│   ├── shipping_handler.py
│   ├── restriction_handler.py
│   ├── best_offer_handler.py
│   └── global_shipping_handler.py
└── tests/                    # Unit tests
    ├── __init__.py
    └── test_*.py
```

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Aris-Geo/listing-automation.git
   cd listing-automation
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure all reference files are in the correct location:
   - EbayNotListed.xlsx (current unlisted report)
   - EbayNotListed_spec_Done.xlsx (previous day's processed file)
   - 1_PlatformRestrictions.xlsx (with necessary sheets)
   - SubtitleseBay.xlsx (subtitle reference file)

## 🔧 Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Load and process the eBay unlisted report
2. Apply all business rules and transformations
3. Generate a processed file: `EbayNotListed_processed_YYYYMMDD_HHMMSS.xlsx`
4. Create exception reports for items requiring manual attention

## 📊 Output Files

The automation generates these files:
- **Main processed file**: `EbayNotListed_processed_YYYYMMDD_HHMMSS.xlsx`
- **Exception reports** (only created if needed):
  - `missing_fields_YYYYMMDD_HHMMSS.xlsx`: Items with missing required data
  - `dimension_updates_YYYYMMDD_HHMMSS.xlsx`: Items needing dimension updates in Seller Cloud
  - `quantity_updates_YYYYMMDD_HHMMSS.xlsx`: Items needing quantity updates in Seller Cloud
  - `restricted_skus_YYYYMMDD_HHMMSS.xlsx`: Items that shouldn't be listed on eBay

## 🔄 Business Logic

The workflow implements these key business processes:

1. **Data Validation**
   - Ensures required fields (BrandName, ManufacturerName, Manufacture SKU) are present
   - Identifies and reports missing data for manual update in Seller Cloud

2. **Certified Refurbished Handling**
   - Updates eBayItemCondition from 2500 to 2000 for brands in CR program
   - Applies specific subtitles for Certified Refurbished items

3. **Quantity Management**
   - Identifies items with quantity < 50
   - Generates report for updating to 100 in Seller Cloud

4. **Platform Restrictions**
   - Checks against Do Not List restrictions
   - Handles special cases (Hello Kitty, Kits, In-House Images Only)
   - Generates report of restricted items

5. **Best Offer Rules**
   - Applies rules based on reference file
   - Enforces price-based rules (items under $49.99)
   - Special handling for Certified Refurbished items

6. **Global Shipping Program**
   - Determines eligibility based on restrictions file
   - Applies weight and dimension limitations
   - Assigns appropriate shipping templates

## ⚙️ Configuration

To modify business rules:
1. Update the CR brands list in `main.py`
2. Maintain up-to-date reference files (1_PlatformRestrictions.xlsx, SubtitleseBay.xlsx)

## 🚨 Troubleshooting

Common issues:
- **File not found**: Ensure all reference files are in the project directory
- **Missing columns**: Verify input file structure matches expected format
- **Excel format issues**: Make sure Excel files are properly closed before processing

## 🔜 Future Enhancements

- Seller Cloud API integration for automatic uploading
- Web interface for monitoring and job control
- Scheduled daily execution
- Advanced reporting and analytics

## 📝 License

Internal use only. All rights reserved.
