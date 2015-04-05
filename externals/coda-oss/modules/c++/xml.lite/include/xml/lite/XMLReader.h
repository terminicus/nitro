/* =========================================================================
 * This file is part of xml.lite-c++ 
 * =========================================================================
 * 
 * (C) Copyright 2004 - 2014, MDA Information Systems LLC
 *
 * xml.lite-c++ is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public 
 * License along with this program; If not, 
 * see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef __XML_LITE_XML_READER_H__
#define __XML_LITE_XML_READER_H__

#include "xml/lite/xml_lite_config.h"

#if defined(USE_XERCES)
#  include "xml/lite/XMLReaderXerces.h"
namespace xml
{
namespace lite
{

typedef XMLReaderXerces XMLReader;
}

}
#elif defined(USE_LIBXML)
#  include "xml/lite/XMLReaderLibXML.h"
namespace xml
{
namespace lite
{
typedef XMLReaderLibXML XMLReader;
}
}
#elif defined(USE_EXPAT)
#  include "xml/lite/XMLReaderExpat.h"
namespace xml
{
namespace lite
{
typedef XMLReaderExpat XMLReader;
}
}
#else
  #error XML parser must be set at configure time
#endif

#endif
