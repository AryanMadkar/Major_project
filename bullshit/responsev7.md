# Model Evaluation Report (All Single-Property Messages)

- Generated: 2026-05-29T00:44:57
- Endpoint: http://127.0.0.1:8000/extract
- Total messages: 16
- Overall supported fields: 102/135
- Overall accuracy: 75.56%

## 1. single_property_Dataset/rent/01.md

- Sample accuracy: 87.50% (14/16)

### Original message

```text
🏢 1BHK FLAT ON RENT 🏢
👉🏻 Available Semi Furnished R Flat 1BHK On Rent at Ganesh Chowk, Charkop, kandivali west,
👉🏻 North Facing, with Gas pipe Line Connection
👉🏻 walking Distance of Kandivali Metro Station
💰 Rent 33000/-   &
Deposit of Rs 1,50,000/-
📞 Please Contact :
BHOOMI ASSOCAITES
9867722289
7977756496
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": "north",
    "furnishing": "semi_furnished"
  },
  "location": {
    "locations": [
      "kandivali west",
      "charkop",
      "ganesh chowk"
    ],
    "primary_location": "kandivali west",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [
      "7977756496",
      "9867722289"
    ],
    "contact_people": [
      "bhoomi associates"
    ],
    "message_title": "1BHK Apartment For Rent in Charkop",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 1,
      "total_numbers": 2
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": 150000,
    "price": 33000,
    "price_max": null,
    "price_min": null,
    "rent_price": 33000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "rent"
  }
}
```

## 2. single_property_Dataset/rent/02.md

- Sample accuracy: 80.00% (8/10)

### Original message

```text
1 bhk fully furnished in blue empire@36000 negotiable

For more details Contact
Rajan sarawagi
9821452541
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "location": {
    "locations": [
      "blue empire"
    ],
    "primary_location": "blue empire",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [
      "9821452541"
    ],
    "contact_people": [
      "rajan sarawagi"
    ],
    "message_title": "1BHK Apartment For Rent",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 1,
      "total_numbers": 1
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 36000,
    "price_max": null,
    "price_min": null,
    "rent_price": 36000
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "rent"
  }
}
```

## 3. single_property_Dataset/rent/03.md

- Sample accuracy: 85.71% (6/7)

### Original message

```text
🏠 2 bhk for rent in veena smart homes@49000

Semi furnished flat
Family preferred
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Rent",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 49000,
    "price_max": null,
    "price_min": null,
    "rent_price": 49000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "rent"
  }
}
```

## 4. single_property_Dataset/rent/04.md

- Sample accuracy: 90.00% (9/10)

### Original message

```text
3 bhk on rent in hiranandani heritage, sv road, poisar, @90000

Fully furnished
Higher floor
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "location": {
    "locations": [
      "poisar",
      "hiranandani heritage",
      "sv road"
    ],
    "primary_location": "poisar",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment For Rent in Sv Road",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 90000,
    "price_max": null,
    "price_min": null,
    "rent_price": 90000
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "rent"
  }
}
```

## 5. single_property_Dataset/rent/049.md

- Sample accuracy: 55.56% (5/9)

### Original message

```text
2 Bhk Rental Flat In Uk Iridium
Semi Furnished Flat With Modular Kitchen
Rent 45k Deposit 1.25 lakh
```

### Model response

```json
{
  "amenities": [
    "modular kitchen"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Rent",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": 125000,
    "price": 45000,
    "price_max": null,
    "price_min": null,
    "rent_price": 45000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "flat"
  },
  "summary": {
    "bhk": 2,
    "request_type": "rent"
  }
}
```

## 6. single_property_Dataset/requirements/01.md

- Sample accuracy: 63.64% (7/11)

### Original message

```text
OM SAI RAM
🏠REQUIRED 1 BHK FLAT FOR OUT RATE BUDGET 1 CR TO 1.10 CR
LOCATION ANY CHARKOP SECTOR
KANDIVALI WEST

CALL
9820067788
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [
      "charkop",
      "kandivali west"
    ],
    "primary_location": "kandivali west",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [
      "9820067788"
    ],
    "contact_people": [],
    "message_title": "1BHK Apartment in Charkop",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 1
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 10000000,
    "price_max": 11000000,
    "price_min": 10000000,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "requirement"
  }
}
```

## 7. single_property_Dataset/requirements/02.md

- Sample accuracy: 83.33% (5/6)

### Original message

```text
Need 2 bhk flat on rent
Budget 45000
Near metro preferred
Family client

Contact urgently
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 45000,
    "price_max": null,
    "price_min": null,
    "rent_price": 45000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "requirement"
  }
}
```

## 8. single_property_Dataset/requirements/03.md

- Sample accuracy: 66.67% (6/9)

### Original message

```text
Urgent Requirement

3 bhk furnished flat required in Borivali West
Budget 2.5 cr
Immediate closing

Broker pls contact
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "location": {
    "locations": [
      "borivali",
      "borivali west"
    ],
    "primary_location": "borivali",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment in Borivali",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 25000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "requirement"
  }
}
```

## 9. single_property_Dataset/requirements/04.md

- Sample accuracy: 60.00% (3/5)

### Original message

```text
Requirement for investor client

Need 2 bhk flat for outright purchase
Budget upto 2 cr
Ready possession only
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 20000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "requirement"
  }
}
```

## 10. single_property_Dataset/requirements/049.md

- Sample accuracy: 83.33% (5/6)

### Original message

```text
Need commercial office on rent
300 carpet minimum
Near link road preferred

Immediate possession required
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [
      "link road"
    ],
    "primary_location": "link road",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Office in Link Road",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "commercial_space",
      "office"
    ],
    "property_subtype": "office"
  },
  "summary": {
    "bhk": null,
    "request_type": "requirement"
  }
}
```

## 11. single_property_Dataset/requirements/06.md

- Sample accuracy: 100.00% (6/6)

### Original message

```text
Client Requirement

Need 4 bhk bungalow in Lonavala
Budget flexible
Ready to move preferred
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [
      "lonavala"
    ],
    "primary_location": "lonavala",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "4BHK Bungalow",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "bungalow"
    ],
    "property_subtype": "bungalow"
  },
  "summary": {
    "bhk": 4,
    "request_type": "requirement"
  }
}
```

## 12. single_property_Dataset/sale/01.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
1 BHK
Kanakya park
With car parking
Asking 1.05 Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "1BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 10500000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "sale"
  }
}
```

## 13. single_property_Dataset/sale/02.md

- Sample accuracy: 55.56% (5/9)

### Original message

```text
2 BHK
Radha residency
With car parking
Furnished flat
Asking 2.85 CR
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 28500000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "sale"
  }
}
```

## 14. single_property_Dataset/sale/03.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
3 BHK
Oberoi sky City
Middle floor
2 car parking
Asking 4.7Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 2,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 47000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "sale"
  }
}
```

## 15. single_property_Dataset/sale/04.md

- Sample accuracy: 66.67% (4/6)

### Original message

```text
🔹 3 BHK | 1036 Sqft | 22nd Floor
💰 ₹3.78 Cr
✅ OC June 2025 | Immediate Possession | 1 Parking
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "3BHK Apartment For Sale",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 37800000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "sale"
  }
}
```

## 16. single_property_Dataset/sale/06.md

- Sample accuracy: 81.82% (9/11)

### Original message

```text
2 BHK
Rizvi Cedar Tower
Malad East
Semi furnished
With car parking
Asking 1.62 Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "location": {
    "locations": [
      "malad",
      "malad east"
    ],
    "primary_location": "malad east",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "2BHK Apartment For Sale in 2 Bhk Rizvi Cedar Tower",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 16200000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "sale"
  }
}
```
