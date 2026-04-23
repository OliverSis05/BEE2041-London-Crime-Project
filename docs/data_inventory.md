# Data Inventory

## Crime data
- Saved in: data/raw/crime/
- Purpose: main borough-month-crime dataset
- Merge keys: borough, year, month, crime_type

## Population data
- Saved in: data/raw/population/
- Purpose: create crime rate per 1,000 residents
- Merge keys: borough, year

## Density data
- Saved in: data/raw/density/
- Purpose: borough-level structural variable
- Merge keys: borough

## Labour-market data
- Saved in: data/raw/labour/
- Purpose: borough-level monthly labour pressure proxy
- Merge keys: borough, year, month

## Deprivation data
- Saved in: data/raw/deprivation/
- Purpose: borough-level socioeconomic proxy
- Merge keys: borough

## Optional earnings data
- Saved in: data/raw/optional/
- Purpose: optional extension / robustness check
- Merge keys: borough, year
